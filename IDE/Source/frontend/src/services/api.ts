export async function api<T>(path:string, method='GET', body?:unknown):Promise<T> {
  const response = await fetch(`/api${path}`, {method, headers:body === undefined ? {} : {'Content-Type':'application/json'}, body:body === undefined ? undefined : JSON.stringify(body)});
  if(!response.ok) {
    if(response.status===401&&!path.startsWith('/auth/'))window.dispatchEvent(new Event('devforge:session-expired'));
    const error = await response.json().catch(()=>({detail:response.statusText}));
    throw new Error(typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail));
  }
  return response.status===204 ? undefined as T : response.json();
}
