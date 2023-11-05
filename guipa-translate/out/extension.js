"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = __importStar(require("vscode"));
const axios_1 = __importDefault(require("axios"));
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
async function activate(context) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        return;
    }
    let disposable = await vscode.commands.registerCommand('extension.sayHello', async () => {
        // O código que você quer executar quando o comando do menu de contexto é acionado
        const selection = editor.selection;
        const text = editor.document.getText(selection);
        const response = (0, axios_1.default)({
            method: 'get',
            url: "http://127.0.0.1:5000/api/v1/translate?input=" + text,
        }).then(response => {
            if (response.status === 200) {
                response.data;
                const endPos = selection.end;
                editor.edit(editBuilder => {
                    // Insert a new line and 'Hello World' at the end of 'hi'
                    editBuilder.insert(endPos, '\n\n' + response.data);
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
exports.activate = activate;
// This method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map