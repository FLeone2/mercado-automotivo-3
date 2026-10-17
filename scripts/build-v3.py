"""Rebuild version 3 maintained sources and verify the final inline CSP hashes."""
from pathlib import Path
import json,re,subprocess,sys
root=Path(__file__).resolve().parents[1]
for script in ['build-scenarios.py','build-animations.py']:
 subprocess.run([sys.executable,str(root/'scripts'/script)],check=True)
p=root/'index.html';s=p.read_text().replace("tab==='models'?jsxRuntime.jsx(ScenarioWorkspace,","tab==='models'?jsxRuntime.jsx(ContextEconomicWorkspace,");start,end='// BEGIN MARKET V3','// END MARKET V3'
block=start+'\n'+'\n'.join((root/'src'/name).read_text() for name in ['v3-analytics.js','v3-ui.js','v3-maps.js'])+'\n'+end
if start in s:s=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:block,s,flags=re.S)
else:s=s.replace('function useMarketData(',block+'\nfunction useMarketData(',1)
css='<style id="market-v3-styles">\n'+(root/'src/v3.css').read_text()+'\n</style>'
if '<style id="market-v3-styles">' in s:s=re.sub(r'<style id="market-v3-styles">.*?</style>',lambda _:css,s,flags=re.S)
else:s=s.replace('</head>',css+'\n</head>',1)
# Theme-aware categorical colors follow actual foreground luminance for all built-in themes.
theme="""\nfunction installV3Theme(){const update=()=>{const raw=getComputedStyle(document.documentElement).getPropertyValue('--text').trim();const canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');if(!ctx)return;ctx.fillStyle=raw||'#172b45';const value=ctx.fillStyle;let rgb;if(value.startsWith('#')){let hex=value.slice(1);if(hex.length===3)hex=hex.split('').map(c=>c+c).join('');rgb=[0,2,4].map(i=>parseInt(hex.slice(i,i+2),16));}else rgb=value.match(/[\\d.]+/g)?.slice(0,3).map(Number);document.documentElement.dataset.v3Dark=String(rgb?.length===3&&(rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722)>150);};new MutationObserver(update).observe(document.documentElement,{attributes:true,attributeFilter:['data-app-theme','class','style']});update();}if(typeof document!=='undefined'&&typeof MutationObserver!=='undefined'&&typeof getComputedStyle!=='undefined')setTimeout(installV3Theme,0);\n"""
s=s.replace(end,theme+end,1);p.write_text(s)
subprocess.run([sys.executable,str(root/'scripts/build-navigation.py')],check=True)
subprocess.run([sys.executable,str(root/'scripts/build-page-notes.py')],check=True)
print('Version 3 embedded; reviewed data preserved.')
