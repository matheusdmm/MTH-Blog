export const defaultLang = 'pt-br' as const;

export const ui = {
  'pt-br': {
    'nav.home': 'Home',
    'nav.blog': 'Blog',
    'nav.projects': 'Projetos',
    'nav.about': 'Sobre',
    'lang.toggle': 'EN',
    'lang.current': 'pt-br',
    'post.lastUpdated': 'Última atualização em',
    'site.description': 'Meu espaço, seja bem-vindo!',
    'footer.rights': 'Todos os direitos reservados.',
  },
  en: {
    'nav.home': 'Home',
    'nav.blog': 'Blog',
    'nav.projects': 'Projects',
    'nav.about': 'About',
    'lang.toggle': 'PT',
    'lang.current': 'en',
    'post.lastUpdated': 'Last updated on',
    'site.description': 'My place, be welcome!',
    'footer.rights': 'All rights reserved.',
  },
} as const;

export type Locale = keyof typeof ui;
export type TranslationKey = keyof typeof ui['en'];

export function useTranslations(lang: Locale) {
  return function t(key: TranslationKey): string {
    return (ui[lang] as Record<string, string>)[key] ?? (ui[defaultLang] as Record<string, string>)[key];
  };
}

export function getLangFromUrl(url: URL): Locale {
  const segments = url.pathname.split('/').filter(Boolean);
  if (segments[0] === 'en') return 'en';
  return defaultLang;
}

export function getOtherLocaleUrl(pathname: string, targetLang: Locale): string {
  if (targetLang === 'en') {
    return `/en${pathname === '/' ? '' : pathname}`;
  }
  return pathname.replace(/^\/en/, '') || '/';
}
