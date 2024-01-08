import { dev } from '$app/environment';

export const WEBUI_BASE_URL = dev ? `http://${location.hostname}:8080` : ``;

export const WEBUI_API_BASE_URL = `${WEBUI_BASE_URL}/api/v1`;
export const OLLAMA_API_BASE_URL = `${WEBUI_BASE_URL}/ollama/api`;
export const OPENAI_API_BASE_URL = `${WEBUI_BASE_URL}/openai/api`;
export const RAG_API_BASE_URL = `${WEBUI_BASE_URL}/rag/api/v1`;

export const WEB_UI_VERSION = 'v1.0.0-alpha-static';

export const REQUIRED_OLLAMA_VERSION = '0.1.16';

export const SUPPORTED_FILE_TYPE = [
	'application/pdf',
	'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
	'text/plain',
	'text/csv'
];

// Source: https://kit.svelte.dev/docs/modules#$env-static-public
// This feature, akin to $env/static/private, exclusively incorporates environment variables
// that are prefixed with config.kit.env.publicPrefix (usually set to PUBLIC_).
// Consequently, these variables can be securely exposed to client-side code.

// Example of the .env configuration:
// OLLAMA_API_BASE_URL="http://localhost:11434/api"
// # Public
// PUBLIC_API_BASE_URL=$OLLAMA_API_BASE_URL
