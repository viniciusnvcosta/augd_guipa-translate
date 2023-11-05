// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import axios from 'axios';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {
	const editor = vscode.window.activeTextEditor;

	if (!editor) {
		return;
	}

	let disposable = await vscode.commands.registerCommand('extension.sayHello', async () => {
		// O código que você quer executar quando o comando do menu de contexto é acionado
		const selection = editor.selection;
		const text = editor.document.getText(selection);

		const response = axios({
			method: 'get',
			url: "http://127.0.0.1:5000/api/v1/translate?input=" + text,
		}).then(response => {
			if (response.status === 200) {
				response.data;

				const endPos = selection.end;
				editor.edit(editBuilder => {

					// Insert a new line and 'Hello World' at the end of 'hi'
					editBuilder.insert(endPos, '\n\n'+response.data);
				}).then(success => {
					// After editing, move the cursor to the end of 'Hello World'
					if (success) {
						const newPosition = endPos.with(endPos.line + 1, 0);
						editor.selection = new vscode.Selection(newPosition, newPosition);
					}
				});

			}


		}).catch(error => {
			// API has returned an error
			const strError = `Taxi for Email: ${error.response.status} - ${error.response.statusText}`;
			console.log(strError);
			vscode.window.showErrorMessage(strError);
		});

	});



	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() { }
