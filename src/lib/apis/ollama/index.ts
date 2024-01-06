import { OLLAMA_API_BASE_URL } from '$lib/constants';

export const getOllamaAPIUrl = async (token: string = '') => {
	let error = null;

	const res = await fetch(`${OLLAMA_API_BASE_URL}/url`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			...(token && { authorization: `Bearer ${token}` })
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			if ('detail' in err) {
				error = err.detail;
			} else {
				error = 'Server connection failed';
			}
			return null;
		});

	if (error) {
		throw error;
	}

	return res.OLLAMA_API_BASE_URL;
};

export const updateOllamaAPIUrl = async (token: string = '', url: string) => {
	let error = null;

	const res = await fetch(`${OLLAMA_API_BASE_URL}/url/update`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			...(token && { authorization: `Bearer ${token}` })
		},
		body: JSON.stringify({
			url: url
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			if ('detail' in err) {
				error = err.detail;
			} else {
				error = 'Server connection failed';
			}
			return null;
		});

	if (error) {
		throw error;
	}

	return res.OLLAMA_API_BASE_URL;
};

export const getOllamaVersion = async (token: string = '') => {
	let error = null;

	const res = await fetch(`${OLLAMA_API_BASE_URL}/version`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			...(token && { authorization: `Bearer ${token}` })
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			if ('detail' in err) {
				error = err.detail;
			} else {
				error = 'Server connection failed';
			}
			return null;
		});

	if (error) {
		throw error;
	}

	return res?.version ?? '';
};

export const getOllamaModels = async (token: string = '') => {
	let error = null;

	const res = await fetch(`${OLLAMA_API_BASE_URL}/tags`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			...(token && { authorization: `Bearer ${token}` })
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			if ('detail' in err) {
				error = err.detail;
			} else {
				error = 'Server connection failed';
			}
			return null;
		});

	if (error) {
		throw error;
	}

	return (res?.models ?? []).sort((a, b) => {
		return a.name.localeCompare(b.name);
	});
};

export const generateTitle = async (token: string = '', model: string, prompt: string) => {
	let error = null;

	const res = await fetch(`${OLLAMA_API_BASE_URL}/generate`, {
		method: 'POST',
		headers: {
			'Content-Type': 'text/event-stream',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			model: model,
			prompt: `Create a concise, 3-5 word phrase as a header for the following query, strictly adhering to the 3-5 word limit and avoiding the use of the word 'title': ${prompt}`,
			stream: false
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			if ('detail' in err) {
				error = err.detail;
			}
			return null;
		});

	if (error) {
		throw error;
	}

	return res?.response ?? 'New Chat';
};

export const generateChatCompletion = async (token: string = '', body: object) => {
	let error = null;

	const res = await fetch(`${OLLAMA_API_BASE_URL}/chat`, {
		method: 'POST',
		headers: {
			'Content-Type': 'text/event-stream',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify(body)
	}).catch((err) => {
		error = err;
		return null;
	});

	if (error) {
		throw error;
	}

	return res;
};

export const createModel = async (token: string, tagName: string, content: string) => {
	let error = null;

	const res = await fetch(`${OLLAMA_API_BASE_URL}/create`, {
		method: 'POST',
		headers: {
			'Content-Type': 'text/event-stream',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			name: tagName,
			modelfile: content
		})
	}).catch((err) => {
		error = err;
		return null;
	});

	if (error) {
		throw error;
	}

	return res;
};

export const deleteModel = async (token: string, tagName: string) => {
	let error = null;

	const res = await fetch(`${OLLAMA_API_BASE_URL}/delete`, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'text/event-stream',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			name: tagName
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			console.log(json);
			return true;
		})
		.catch((err) => {
			console.log(err);
			error = err.error;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const pullModel = async (token: string, tagName: string) => {
	let error = null;

	const res = await fetch(`${OLLAMA_API_BASE_URL}/pull`, {
		method: 'POST',
		headers: {
			'Content-Type': 'text/event-stream',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			name: tagName
		})
	}).catch((err) => {
		console.log(err);
		error = err;

		if ('detail' in err) {
			error = err.detail;
		}

		return null;
	});
	if (error) {
		throw error;
	}
	return res;
};

// export const pullModel = async (token: string, tagName: string) => {
// 	return await fetch(`${OLLAMA_API_BASE_URL}/pull`, {
// 		method: 'POST',
// 		headers: {
// 			'Content-Type': 'text/event-stream',
// 			Authorization: `Bearer ${token}`
// 		},
// 		body: JSON.stringify({
// 			name: tagName
// 		})
// 	});
// };
