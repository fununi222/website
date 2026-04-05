/**
 * FunUni-lab Synthetic Edition - Shared Tailwind Config
 */
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                'primary': '#aaa4ff',
                'primary-dim': '#6a5cf9',
                'secondary': '#00d2ff',
                'tertiary': '#b0aaff',
                'background': '#060e20',
                'surface': '#0f1930',
                'surface-container': '#141f38',
                'on-surface': '#dee5ff',
                'on-surface-variant': '#a3aac4',
                'outline': '#6d758c'
            },
            fontFamily: {
                headline: ['Space Grotesk'],
                body: ['Inter']
            }
        }
    }
};
