const ROOT_API = proecss.env.VUE_APP_ROOT_API;
const apiUrl = method => `${ROOT_API}${method}`;

export const postSeedText = (sessionId, text) =>
	fetch(apiUrl(`${sessionId}/texts`), {
		method: 'POST',
		body: JSON.stringify({ text }),
	});

export const postCommentAnnotation = (sessionId, commentId, positive) =>
	fetch(apiUrl(`${sessionId}/comments`), {
		method: 'POST',
		body: JSON.stringify({ id: commentId, positive }),
	});


export const putUpdateConcept = (sessionId, concepId) =>
	fetch(apiUrl(`${sessionId}/update`), {
		method: 'PUT',
		body: JSON.stringify({ id: concepId }),
	});