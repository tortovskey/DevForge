import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import tailwind from '@tailwindcss/vite';
export default defineConfig({plugins:[react(),tailwind(),{
  name:'devforge-worker-isolation',
  configureServer(server){server.middlewares.use((request,response,next)=>{
    if(request.url?.startsWith('/workers/')||request.url?.startsWith('/runtimes/')){
      const origin=`http://${request.headers.host}`;
      response.setHeader('Content-Security-Policy',`default-src 'none'; script-src ${origin}/runtimes/ blob: 'unsafe-eval'; connect-src ${origin}/runtimes/ ${origin}/workers/backend_pack.py; worker-src ${origin}/runtimes/ blob:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`);
    }
    next();
  });}
}],server:{port:5173,strictPort:true,headers:{'Cross-Origin-Opener-Policy':'same-origin','Cross-Origin-Embedder-Policy':'require-corp'},proxy:{'/api':process.env.DEVFORGE_API||'http://127.0.0.1:8000'}},build:{
  chunkSizeWarningLimit:3000,
  rollupOptions:{
    output:{
      manualChunks:{
        monaco:['monaco-editor'],
        reactVendor:['react','react-dom','react-router-dom']
      }
    }
  }
}});
