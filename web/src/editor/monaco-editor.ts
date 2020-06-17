import CodeMirror from 'codemirror';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/mode/yaml/yaml';
import monokai from 'codemirror/theme/monokai.css';
import { CtLit, html, property, customElement, css, unsafeHTML } from '@conectate/ct-lit/ct-lit';
import { codeMirrorEditorCSS } from './CSSMirrorEditorStyles';

@customElement('monaco-editor')
export class MonacoEditor extends CtLit {
	static styles = [
		codeMirrorEditorCSS,
		css`
			:host {
				display: block;
			}
			.CodeMirror {
				height: 500px;
			}
			#editor {
				height: 600px;
				width: 600px;
			}
		`
	];
	@property({ type: String }) value = `main: 
    $t1=0;
    $t2=0;
while:
    if ($t1>=4) goto end; 
    $t2 = $t2 + $t1;
    $t1 = $t1 + 1;
    goto while;
end: 
    print($t2);`;
	code_editor!: CodeMirror.EditorFromTextArea;

	render() {
		return html`${unsafeHTML(`<style>${monokai}</style>`)} <textarea id="editor"></textarea>`;
	}
	firstUpdated() {
		this.mapIDs();
		this.setupEel();
		this.setEditorText(this.value);
		this.code_editor = CodeMirror.fromTextArea(this.$.editor, {
			theme: 'monokai',
			value: 'function myScript(){return 100;}\n',
			lineNumbers: true,
			gutters: ['CodeMirror-linenumbers', 'breakpoints'],
			mode: 'yaml'
		});

		this.code_editor.on('gutterClick', (cm, n) => {
			const info = cm.lineInfo(n);
			this.setBreakPoint(info.line, info.gutterMarkers === undefined);
			cm.setGutterMarker(n, 'breakpoints', info.gutterMarkers ? null : this.makeMarker());
		});
	}

	setupEel() {
		window.eel?.expose(this.setEditorText.bind(this), 'setEditorText');
		window.eel?.expose(this.getEditorText.bind(this), 'getEditorText');
		window.eel._init();
	}

	setEditorText(text: string) {
		this.$.editor.value = this.value;
	}
	getEditorText() {
		return this.$.editor.value;
	}

	makeMarker() {
		const marker = document.createElement('div');
		marker.style.color = '#822';
		marker.innerHTML = '●';
		return marker;
	}

	breakPoints: number[] = [];
	setBreakPoint(_info: number, _delete: boolean) {
		if (_delete) {
			this.breakPoints.push(_info + 1);
			this.breakPoints.sort();
		} else {
			const idx = this.breakPoints.indexOf(_info + 1);
			this.breakPoints.splice(idx, 1);
			this.breakPoints.sort();
			// Interpreter.setBreakPoint(this.breakPoints);
		}
	}
}
