// donate.js — copy-to-clipboard and helper for donate.html
(function(){
  function $(s){return document.querySelector(s)}
  function createToast(msg){
    var existing = document.getElementById('donate-toast');
    if(existing){ existing.textContent = msg; existing.style.opacity = '1'; clearTimeout(existing._t); existing._t = setTimeout(()=> existing.style.opacity='0',2500); return; }
    var t = document.createElement('div');
    t.id = 'donate-toast';
    t.textContent = msg;
    t.style.position = 'fixed';
    t.style.bottom = '80px';
    t.style.right = '16px';
    t.style.background = '#111';
    t.style.color = '#cfe';
    t.style.padding = '10px 14px';
    t.style.borderRadius = '6px';
    t.style.boxShadow = '0 4px 16px rgba(0,0,0,.6)';
    t.style.zIndex = 10000;
    t.style.transition = 'opacity .3s';
    document.body.appendChild(t);
    t._t = setTimeout(()=> t.style.opacity='0',2500);
  }

  function copyText(text){
    if(!navigator.clipboard){
      // fallback
      var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); try{ document.execCommand('copy'); createToast('Скопировано в буфер'); }catch(e){ createToast('Копирование не удалось'); } ta.remove();
    } else {
      navigator.clipboard.writeText(text).then(function(){ createToast('Скопировано в буфер'); }, function(){ createToast('Копирование не удалось'); });
    }
  }

  document.addEventListener('DOMContentLoaded', function(){
    var pre = document.querySelector('#bank-rect');
    if(!pre) return;
    var copyBtn = document.createElement('button');
    copyBtn.textContent = 'Копировать реквизиты';
    copyBtn.style.marginTop = '8px';
    copyBtn.style.marginRight = '8px';
    copyBtn.className = 'button';
    copyBtn.onclick = function(){ copyText(pre.innerText); };

    var purposeText = document.querySelector('#payment-purpose');
    var copyPurposeBtn = document.createElement('button');
    copyPurposeBtn.textContent = 'Копировать назначение платежа';
    copyPurposeBtn.style.marginTop = '8px';
    copyPurposeBtn.className = 'button';
    copyPurposeBtn.onclick = function(){ copyText(purposeText.innerText); };

    pre.parentNode.insertBefore(copyBtn, pre.nextSibling);
    pre.parentNode.insertBefore(copyPurposeBtn, copyBtn.nextSibling);

    // security warning toggle
    var warn = document.querySelector('#phish-warn');
    if(warn){ warn.style.display='block'; }
  });
})();
