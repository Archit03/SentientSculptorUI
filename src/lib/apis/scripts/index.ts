import { WEBUI_API_BASE_URL } from '$lib/constants';

export const createNewPyScripts = async (token: string, func: object) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/functions/create`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      ...func
    })
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      error = err.detail;
      console.log(err);
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};

export const getPyScripts = async (token: string = '') => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/functions/`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    }
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .then((json) => {
      return json;
    })
    .catch((err) => {
      error = err.detail;
      console.log(err);
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};

export const getPyScriptById = async (token: string, id: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/functions/id/${id}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    }
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .then((json) => {
      return json;
    })
    .catch((err) => {
      error = err.detail;

      console.log(err);
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};

export const updatePyScriptById = async (token: string, id: string, func: object) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/functions/id/${id}/update`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      ...func
    })
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .then((json) => {
      return json;
    })
    .catch((err) => {
      error = err.detail;

      console.log(err);
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};

export const deletePyScriptById = async (token: string, id: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/functions/id/${id}/delete`, {
    method: 'DELETE',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    }
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .then((json) => {
      return json;
    })
    .catch((err) => {
      error = err.detail;

      console.log(err);
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};