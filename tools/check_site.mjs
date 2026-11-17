#!/usr/bin/env node
// Read-only availability and configuration checks. Does not submit leads or prove malware-free status.
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
const base = 'https://restoregleam.vip/';
const pages = ['','interior-detailing-chicago.html','paint-correction-chicago.html','ceramic-coating-chicago.html','headlight-restoration-chicago.html','boat-detailing-chicago.html','robots.txt','sitemap.xml'];
const live = process.argv.includes('--live');
const results = [];
const check = (name, ok, detail='') => results.push({name,ok,detail});
function inspect(path, html) {
  if (!path.endsWith('.txt') && !path.endsWith('.xml')) {
    check(path+' canonical', html.includes('rel="canonical" href="'+base+path+'"'));
    check(path+' contact', html.includes('847') && html.includes('964') && html.includes('3474'));
    check(path+' intake', html.includes('id="quote-form"') && html.includes('script.google.com/macros/s/') && html.includes("res.status === 'ok'"));
    for (const match of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
      try {JSON.parse(match[1]); check(path+' JSON-LD',true);} catch {check(path+' JSON-LD',false);}
    }
  }
}
for (const path of pages) {
  if (!live) {
    const file = path || 'index.html';
    check(file+' exists', existsSync(file));
    if (existsSync(file)) inspect(path, readFileSync(file,'utf8'));
    continue;
  }
  let lastError = '';
  for (let attempt=1; attempt<=3; attempt++) {
    try {
      const response = await fetch(base+path,{signal:AbortSignal.timeout(20000),redirect:'follow'});
      if (!response.ok) throw new Error('HTTP '+response.status);
      const final = new URL(response.url);
      if (final.protocol !== 'https:' || final.hostname !== 'restoregleam.vip') throw new Error('unexpected redirect');
      const html = await response.text();
      check(path||'homepage',true,'HTTP '+response.status);
      inspect(path,html);
      lastError=''; break;
    } catch (error) { lastError=error.name+': '+error.message; }
  }
  if (lastError) check(path||'homepage',false,lastError);
}
const report = {checked_at:new Date().toISOString(),mode:live?'live-read-only':'repository',scope:'HTTP/configuration only; no form submission, CRM delivery or security certification',ok:results.every(x=>x.ok),results};
mkdirSync('health-reports',{recursive:true});
writeFileSync('health-reports/latest.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
if (!report.ok) process.exitCode=1;
