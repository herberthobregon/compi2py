import { CtLit, html, property, customElement, css } from '@conectate/ct-lit/ct-lit';
import './editor/monaco-editor';
import './base/styles/default-theme';

@customElement('usac-app')
export class UsacApp extends CtLit {
	static styles = css`
		:host {
			display: block;
		}
	`;

	render() {
		return html`
			<h1>OLC2.</h1>
			<monaco-editor></monaco-editor>
		`;
	}

	async firstUpdated() {
		console.log('Calling Python...');
		
		// console.log(window.eel?._exposed_functions);
		// let a = window.eel?.save_data()!;
	}
}
