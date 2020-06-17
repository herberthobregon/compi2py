export let a = 1;
declare global {
	interface eel {
		[x: string]: (...args: any) => (...args: any) => any;
	}
	interface Window {
		eel?: {
			expose: (f: Function, name: string) => any;
			[x: string]: (...args: any) => (...args: any) => Promise<any>;
		};
	}
}
