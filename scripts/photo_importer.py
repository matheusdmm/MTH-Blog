"""Import photographs into the Astro img collection with a small Tkinter editor."""

from __future__ import annotations

import json
import re
import unicodedata
import webbrowser
from datetime import date, datetime
from pathlib import Path
from tkinter import BooleanVar, StringVar, Text, Tk, filedialog, messagebox, ttk
import tkinter as tk
from urllib.error import URLError
from urllib.request import urlopen

from PIL import ExifTags, Image, ImageOps, ImageTk


GALLERY = Path(__file__).resolve().parents[1] / "src" / "content" / "img"
FORMATS = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}


def slugify(value: str) -> str:
    plain = unicodedata.normalize("NFKD", value)
    plain = "".join(char for char in plain if not unicodedata.combining(char))
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", plain.lower()))


def title_from_filename(path: Path) -> str:
    words = re.sub(r"[_-]+", " ", path.stem).strip()
    return words[:1].upper() + words[1:]


def exif_date(exif) -> str | None:
    detail = exif.get_ifd(ExifTags.IFD.Exif)
    for value in (
        detail.get(ExifTags.Base.DateTimeOriginal),
        detail.get(ExifTags.Base.DateTimeDigitized),
        exif.get(ExifTags.Base.DateTime),
    ):
        if not value:
            continue
        try:
            return datetime.strptime(str(value)[:19], "%Y:%m:%d %H:%M:%S").date().isoformat()
        except ValueError:
            continue
    return None


def _coordinate(parts, reference: str) -> float:
    degrees, minutes, seconds = (float(part) for part in parts)
    value = degrees + minutes / 60 + seconds / 3600
    return -value if reference.upper() in {"S", "W"} else value


def exif_gps(exif) -> tuple[float, float] | None:
    try:
        gps = exif.get_ifd(ExifTags.IFD.GPSInfo)
        lat_ref = gps[ExifTags.GPS.GPSLatitudeRef]
        lon_ref = gps[ExifTags.GPS.GPSLongitudeRef]
        if isinstance(lat_ref, bytes):
            lat_ref = lat_ref.decode("ascii")
        if isinstance(lon_ref, bytes):
            lon_ref = lon_ref.decode("ascii")
        latitude = _coordinate(gps[ExifTags.GPS.GPSLatitude], lat_ref)
        longitude = _coordinate(gps[ExifTags.GPS.GPSLongitude], lon_ref)
        if -90 <= latitude <= 90 and -180 <= longitude <= 180:
            return latitude, longitude
    except (KeyError, TypeError, ValueError, ZeroDivisionError, AttributeError):
        pass
    return None


def frontmatter(
    image_name: str,
    title: str,
    caption: str,
    alt: str,
    photo_date: str,
    tags: list[str],
    location: tuple[str, float, float] | None,
) -> str:
    quoted = lambda value: json.dumps(value, ensure_ascii=False)
    lines = [
        "---",
        f"image: {quoted('./' + image_name)}",
        f"alt: {quoted(alt)}",
        f"caption: {quoted(caption)}",
        f"date: {photo_date}",
        f"title: {quoted(title)}",
    ]
    if tags:
        lines.append("tags: [" + ", ".join(quoted(tag) for tag in tags) + "]")
    if location:
        name, latitude, longitude = location
        lines.extend([
            "location:",
            f"  name: {quoted(name)}",
            f"  latitude: {latitude:.7f}",
            f"  longitude: {longitude:.7f}",
        ])
    return "\n".join([*lines, "---", ""])


def save_photo(source: Path, title: str, caption: str, alt: str, photo_date: str,
               tags: list[str], location: tuple[str, float, float] | None) -> tuple[Path, Path]:
    slug = slugify(title)
    if not slug:
        raise ValueError("O título precisa conter letras ou números para formar a URL.")
    extension = source.suffix.lower()
    if extension not in FORMATS:
        raise ValueError("Use uma imagem JPEG, PNG ou WebP.")
    date.fromisoformat(photo_date)
    GALLERY.mkdir(parents=True, exist_ok=True)
    image_path = GALLERY / f"{slug}{extension}"
    markdown_path = GALLERY / f"{slug}.md"
    if image_path.exists() or markdown_path.exists():
        raise FileExistsError(f"Já existe uma publicação com a URL /img/{slug}. Escolha outro título.")

    # The published copy is oriented correctly and contains no camera/GPS EXIF.
    created_image = False
    created_markdown = False
    try:
        with Image.open(source) as original:
            if original.format != FORMATS[extension]:
                raise ValueError("A extensão não corresponde ao formato real da imagem.")
            image = ImageOps.exif_transpose(original)
            if extension in {".jpg", ".jpeg"} and image.mode not in {"RGB", "L"}:
                image = image.convert("RGB")
            image.info.pop("exif", None)
            with image_path.open("xb") as output:
                created_image = True
                options = {"quality": 92, "optimize": True} if extension in {".jpg", ".jpeg", ".webp"} else {"optimize": True}
                image.save(output, format=FORMATS[extension], **options)
        with markdown_path.open("x", encoding="utf-8", newline="\n") as output:
            created_markdown = True
            output.write(frontmatter(image_path.name, title, caption, alt, photo_date, tags, location))
    except Exception:
        if created_markdown:
            markdown_path.unlink(missing_ok=True)
        if created_image:
            image_path.unlink(missing_ok=True)
        raise
    return image_path, markdown_path


class PhotoImporter:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Img · Importar fotografia")
        self.root.geometry("1060x740")
        self.root.minsize(900, 670)
        self.source: Path | None = None
        self.gps: tuple[float, float] | None = None
        self.preview_image = None

        self.title = StringVar()
        self.date = StringVar()
        self.alt = StringVar()
        self.tags = StringVar()
        self.place = StringVar()
        self.include_location = BooleanVar(value=False)
        self.file_info = StringVar(value="Escolha uma imagem para começar.")
        self.exif_info = StringVar(value="Data e localização EXIF aparecerão aqui.")

        self.build_ui()
        root.bind("<Control-o>", lambda _event: self.choose_image())
        root.bind("<Control-s>", lambda _event: self.save())

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=24)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(1, weight=1)

        heading = ttk.Frame(outer)
        heading.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        ttk.Label(heading, text="Nova imagem", font=("Arial", 20, "bold")).pack(side="left")
        ttk.Button(heading, text="Escolher imagem…", command=self.choose_image).pack(side="right")

        left = ttk.Frame(outer)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 18))
        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)
        self.preview = tk.Label(left, bg="#ffffff", fg="#666666", text="Prévia da foto", font=("Arial", 12))
        self.preview.grid(row=0, column=0, sticky="nsew")
        ttk.Label(left, textvariable=self.file_info, wraplength=450).grid(row=1, column=0, sticky="w", pady=(12, 4))
        ttk.Label(left, textvariable=self.exif_info, wraplength=450, foreground="#666666").grid(row=2, column=0, sticky="w")
        self.map_button = ttk.Button(left, text="Ver ponto no mapa ↗", command=self.open_map)
        self.map_button.grid(row=3, column=0, sticky="w", pady=(12, 0))
        self.map_button.state(["disabled"])

        right = ttk.Frame(outer)
        right.grid(row=1, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        self.field(right, "Título", self.title, 0)
        self.field(right, "Data (AAAA-MM-DD)", self.date, 2)
        self.field(right, "Texto alternativo da imagem", self.alt, 4)
        ttk.Label(right, text="Legenda / descrição").grid(row=6, column=0, sticky="w", pady=(12, 4))
        self.caption = Text(right, height=5, wrap="word", font=("Arial", 10))
        self.caption.grid(row=7, column=0, sticky="ew")
        self.field(right, "Tags (separadas por vírgula, opcional)", self.tags, 8)

        ttk.Separator(right).grid(row=10, column=0, sticky="ew", pady=18)
        self.location_check = ttk.Checkbutton(
            right, text="Publicar localização exata da foto", variable=self.include_location
        )
        self.location_check.grid(row=11, column=0, sticky="w")
        self.location_check.state(["disabled"])
        self.field(right, "Nome do lugar (se publicar localização)", self.place, 12)
        ttk.Label(
            right,
            text="A cópia publicada não guarda EXIF. O local só entra no post se a opção acima estiver marcada.",
            wraplength=430,
            foreground="#666666",
        ).grid(row=14, column=0, sticky="w", pady=(8, 0))

        footer = ttk.Frame(outer)
        footer.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(24, 0))
        ttk.Label(footer, text="O post será salvo em src/content/img/").pack(side="left")
        ttk.Button(footer, text="Salvar na galeria", command=self.save).pack(side="right")

    def field(self, parent, label: str, variable: StringVar, row: int):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=(10, 4))
        ttk.Entry(parent, textvariable=variable).grid(row=row + 1, column=0, sticky="ew")

    def choose_image(self):
        selected = filedialog.askopenfilename(
            title="Escolher fotografia",
            filetypes=[("Fotografias", "*.jpg *.jpeg *.png *.webp"), ("Todos os arquivos", "*.*")],
        )
        if not selected:
            return
        path = Path(selected)
        if path.suffix.lower() not in FORMATS:
            messagebox.showerror("Formato não suportado", "Escolha uma imagem JPEG, PNG ou WebP.")
            return
        try:
            with Image.open(path) as original:
                if original.format != FORMATS[path.suffix.lower()]:
                    raise ValueError("A extensão não corresponde ao formato real da imagem.")
                size = original.size
                exif = original.getexif()
                taken = exif_date(exif)
                gps = exif_gps(exif)
                preview = ImageOps.exif_transpose(original)
                preview.thumbnail((480, 500), Image.Resampling.LANCZOS)
                self.preview_image = ImageTk.PhotoImage(preview)
        except Exception as error:
            messagebox.showerror("Não foi possível abrir a imagem", str(error))
            return

        self.source = path
        self.gps = gps
        self.preview.configure(image=self.preview_image, text="")
        self.title.set(title_from_filename(path))
        self.alt.set(title_from_filename(path))
        self.date.set(taken or date.today().isoformat())
        self.tags.set("")
        self.place.set("")
        self.caption.delete("1.0", "end")
        self.include_location.set(False)
        self.file_info.set(f"{path.name} · {size[0]} × {size[1]} px")
        gps_text = f"{gps[0]:.6f}, {gps[1]:.6f}" if gps else "não encontrada"
        self.exif_info.set(f"Data EXIF: {taken or 'não encontrada'}  ·  GPS: {gps_text}")
        self.map_button.state(["!disabled"] if gps else ["disabled"])
        self.location_check.state(["!disabled"] if gps else ["disabled"])

    def open_map(self):
        if self.gps:
            latitude, longitude = self.gps
            webbrowser.open(f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=14/{latitude}/{longitude}")

    def save(self):
        if not self.source:
            messagebox.showwarning("Falta a imagem", "Escolha uma imagem primeiro.")
            return
        title = self.title.get().strip()
        alt = self.alt.get().strip()
        caption = self.caption.get("1.0", "end-1c").strip()
        photo_date = self.date.get().strip()
        if not all((title, alt, caption, photo_date)):
            messagebox.showwarning("Campos incompletos", "Preencha título, data, texto alternativo e legenda.")
            return
        try:
            date.fromisoformat(photo_date)
        except ValueError:
            messagebox.showerror("Data inválida", "Use uma data no formato AAAA-MM-DD.")
            return
        location = None
        if self.include_location.get():
            if not self.gps or not self.place.get().strip():
                messagebox.showwarning("Local incompleto", "Informe o nome do lugar para publicar a localização.")
                return
            location = (self.place.get().strip(), *self.gps)
        tags = list(dict.fromkeys(tag.strip() for tag in self.tags.get().split(",") if tag.strip()))
        try:
            _image_path, markdown_path = save_photo(
                self.source, title, caption, alt, photo_date, tags, location
            )
        except (OSError, ValueError) as error:
            messagebox.showerror("Não foi possível salvar", str(error))
            return
        preview_url = f"http://localhost:4321/img/{markdown_path.stem}"
        try:
            with urlopen(preview_url, timeout=2) as response:
                preview_available = response.status == 200
        except (OSError, URLError):
            preview_available = False

        if preview_available:
            if messagebox.askyesno(
                "Post criado na galeria",
                f"Post salvo em {markdown_path.name}.\n\nAbrir a prévia local agora?",
            ):
                webbrowser.open(preview_url)
        else:
            messagebox.showinfo(
                "Post criado na galeria",
                f"Post salvo em {markdown_path.name}.\n\n"
                "Para vê-lo no computador, inicie 'bun run dev' e abra /img. "
                "Para vê-lo no site público, é preciso publicar uma nova versão do site.",
            )


if __name__ == "__main__":
    window = Tk()
    PhotoImporter(window)
    window.mainloop()
