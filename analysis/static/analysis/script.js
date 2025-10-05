document.addEventListener("DOMContentLoaded", function(){
  const fileInput = document.getElementById('fileInput');
  const dropzone = document.getElementById('dropzone');
  const fileMeta = document.getElementById('fileMeta');
  const fileNameEl = document.getElementById('fileName');
  const fileSizeEl = document.getElementById('fileSize');
  const clearBtn = document.getElementById('clearBtn');
  const previewBtn = document.getElementById('previewBtn');
  const previewSection = document.getElementById('previewSection');
  const pgnPreview = document.getElementById('pgnPreview');
  const errorEl = document.getElementById('error');

  let selectedFile = null;
  const MAX_BYTES = 5 * 1024 * 1024;

  function bytesToSize(bytes){
    if(bytes === 0) return '0 B';
    const sizes = ['B','KB','MB','GB','TB'];
    const i = Math.floor(Math.log(bytes)/Math.log(1024));
    return (bytes/Math.pow(1024,i)).toFixed(2) + ' ' + sizes[i];
  }

  function showError(msg){
    errorEl.hidden = false;
    errorEl.textContent = msg;
  }
  function clearError(){ errorEl.hidden = true; errorEl.textContent = '' }

  function setFile(file){
    clearError();
    if(!file) return;
    if(file.size > MAX_BYTES){ showError('File is too large. Max size 5 MB.'); return; }
    const name = file.name || 'unknown.pgn';
    const lower = name.toLowerCase();
    if(!(lower.endsWith('.pgn') || lower.endsWith('.txt'))){ showError('Invalid file type. Please upload a .pgn or .txt file.'); return; }

    selectedFile = file;
    fileMeta.hidden = false;
    fileNameEl.textContent = file.name;
    fileSizeEl.textContent = bytesToSize(file.size);
    previewSection.hidden = true;
    pgnPreview.textContent = '';
  }

  if(fileInput){
    fileInput.addEventListener('change', (e)=>{
      const file = e.target.files && e.target.files[0];
      setFile(file);
    });
  }

  ['dragenter','dragover'].forEach(ev => {
    dropzone?.addEventListener(ev, (e)=>{
      e.preventDefault(); e.stopPropagation();
      dropzone.classList.add('dragover');
    });
  });
  ['dragleave','drop'].forEach(ev => {
    dropzone?.addEventListener(ev, (e)=>{
      e.preventDefault(); e.stopPropagation();
      dropzone.classList.remove('dragover');
    });
  });
  dropzone?.addEventListener('drop', (e)=>{
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    setFile(file);
  });

  clearBtn?.addEventListener('click', ()=>{
    selectedFile = null;
    fileInput.value = '';
    fileMeta.hidden = true;
    previewSection.hidden = true;
    pgnPreview.textContent = '';
    clearError();
  });

  previewBtn?.addEventListener('click', ()=>{
    clearError();
    if(!selectedFile){ showError('No file selected.'); return; }

    const reader = new FileReader();
    reader.onload = function(evt){
      const text = evt.target.result;
      if(text.length > 200000){ showError('PGN is very large — preview disabled.'); return; }
      pgnPreview.textContent = text.trim();
      previewSection.hidden = false;
    };
    reader.onerror = function(){ showError('Failed to read file.'); };
    reader.readAsText(selectedFile, 'utf-8');
  });
});
