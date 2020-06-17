import { css } from 'lit-element';
const link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
//link.href = 'https://fonts.googleapis.com/css?family=Product+Sans:500,700';
link.href = 'https://fonts.googleapis.com/css?family=Ubuntu:400,500,700';
document.head.appendChild(link);

const style = document.createElement('style');
export let defaultTheme = css`
	.dark {
		--app-color: linear-gradient(-45deg, #2084e8, #002b5c);
		--app-grad: linear-gradient(-45deg, #2084e8, #002b5c);

		--dark-primary-color: #218cb3;
		--dark-accent-color: #862efb;

		/* Fondos */
		--app-background: #1d1d1d;
		/* Fondos Textos que aparecen en los fondos */
		--on-background: #fff;

		/* Fondos que estan en cima de los fondos (ct-cards) */
		--app-surface: #303030;
		--app-surface-blur: #261a3480;
		/* Fondos Textos que aparecen en los ct-cards */
		--on-surface: #fff;
		--high-emphasis: #ffffffde;
		--medium-emphasis: #fff9;
		--app-disable: #ffffff61;

		--on-surface-opaque: #8e8e8e; /* Texto sencundarios */
		--on-surface-dividers: #bbbbbb24; /* divisores */

		--primary-color: #2084e8;
		--on-primary: #fff;
		--primary-color-medium: #2084e8b0;
		--primary-color-light: #2084e82b;

		--accent-color: #862efb;
		--on-accent: #fff;

		--app-error: #cf6679;
		--on-error: #000000;
	}
`;
style.innerHTML = defaultTheme.cssText;
document.head.appendChild(style);
