import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import { createVuetify } from 'vuetify'

const burningTheme = {
  dark: true,
  colors: {
    background: '#0F0F17',
    surface: '#1A1A2E',
    'surface-bright': '#2D2D44',
    'surface-variant': '#3A3A52',
    primary: '#FF6B6B',
    'primary-darken-1': '#E55A5A',
    secondary: '#4ECDC4',
    'secondary-darken-1': '#3DBDB5',
    error: '#FF5252',
    info: '#64B5F6',
    success: '#69F0AE',
    warning: '#FFD740',
    'on-background': '#EAEAEA',
    'on-surface': '#EAEAEA',
    'on-surface-bright': '#EAEAEA',
    'on-surface-variant': '#D0D0D0',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'burningTheme',
    themes: {
      burningTheme,
    },
  },
  defaults: {
    VBtn: {
      rounded: 'lg',
      variant: 'flat',
    },
    VCard: {
      rounded: 'xl',
      elevation: 0,
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
    },
  },
})
