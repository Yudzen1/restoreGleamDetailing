import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const pages=['index.html','interior-detailing-chicago.html','paint-correction-chicago.html','ceramic-coating-chicago.html','headlight-restoration-chicago.html','boat-detailing-chicago.html'];
async function exercise(file,mode){
 const html=readFileSync(file,'utf8');
 const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(x=>x[1]);
 const script=scripts.find(x=>x.includes("const LEAD_ENDPOINT"));
 assert.ok(script,file+' lead script');
 const start=script.indexOf("document.getElementById('quote-form').addEventListener('submit'");
 const end=script.indexOf('\n});',start)+4;
 const handlerCode=script.slice(start,end);
 let handler,timer,cleared=false,calls=0;
 const events=[];
 const btn={disabled:false,textContent:'Send My Request'};
 const elements=Object.fromEntries(['name','phone','email','service','vehicle','location','notes','company'].map(k=>['quote-'+k,{value:k==='company'?'':k==='service'?'Interior Detailing':'TEST '+k}]));
 elements['quote-output']={textContent:''};
 elements['quote-send']={hidden:true,href:''};
 elements['quote-form']={addEventListener:(event,fn)=>{handler=fn;}};
 const context={
  document:{getElementById:id=>elements[id]},
  LEAD_ENDPOINT:'https://example.invalid/test-only', LEAD_SOURCE:file,
  val:id=>(elements[id].value||'').trim(),
  makeQuote:()=> 'TEST DETAILS',encodeURIComponent,AbortController,
  setTimeout:(fn,ms)=>{assert.equal(ms,30000);timer=fn;return 1;},
  clearTimeout:id=>{assert.equal(id,1);cleared=true;},
  track:(name,params)=>events.push({name,params}),
  fetch:(_url,options)=>{
   calls++;assert.equal(options.method,'POST');assert.ok(options.signal);assert.equal(JSON.parse(options.body).name,'TEST name');
   if(mode==='timeout') return new Promise((_resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new Error('aborted'))));
   if(mode==='error') return Promise.reject(new Error('network response lost'));
   return Promise.resolve({json:()=>Promise.resolve({status:mode==='ok'?'ok':'rejected'})});
  }
 };
 vm.runInNewContext(handlerCode,context);
 const form={querySelector:()=>btn};
 const event={preventDefault(){}};
 handler.call(form,event); handler.call(form,event);
 assert.equal(calls,1,file+' must not double-send');
 if(mode==='timeout')timer();
 for(let i=0;i<12;i++) await Promise.resolve();
 assert.ok(cleared,file+' timer cleared');
 assert.ok(btn.disabled,file+' ambiguous request cannot be resubmitted');
 assert.equal(elements['quote-send'].hidden,false);
 if(mode==='ok'){
  assert.equal(btn.textContent,'Request Sent');
  assert.equal(events.filter(x=>x.name==='conversion').length,1);
 }else{
  assert.match(elements['quote-output'].textContent,/could not confirm whether/);
  assert.equal(btn.textContent,'Please Text or Call');
  assert.equal(events.filter(x=>x.name==='conversion').length,0);
 }
 handler.call(form,event);assert.equal(calls,1,file+' cannot resend after completion');
}
for(const file of pages)for(const mode of ['ok','timeout','error','rejected'])await exercise(file,mode);
console.log('PASS: 24 lead form cases; duplicate events, timeout, uncertain response, rejection, conversion gating.');
