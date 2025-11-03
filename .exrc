" Only for Markdown files
augroup markdown_shortcuts
  autocmd!
  autocmd FileType markdown call s:markdown_mappings()
augroup END

function! s:markdown_mappings()
		" Bold: **text**
		inoremap <buffer> <C-b> ****<Left><Left>
		" Italic: *text*
		inoremap <buffer> <C-i> **<Left>
		" Inline code: `code`
		inoremap <buffer> <C-k> ``<Left>
		" Code block (triple backticks)
		" inoremap <buffer> <C-l> ```<CR><CR>```
		inoremap <buffer> <C-l> ```<CR><CR>```<Esc>kA
		" compile to html

		autocmd!
		" autocmd BufWritePost *.md !pandoc -s % -o %:p:h/index.html --css ../../style.css -V title=""
		" autocmd BufWritePost home.md !pandoc -s % -o %:p:h/index.html --css ./style.css -V title=""
		let s:project_root = expand('<sfile>:p:h')  " directory where this .vimrc/.exrc lives
		autocmd BufWritePost *.md execute '!pandoc -s ' . shellescape(expand('%')) . ' -o ' . shellescape(expand('%:p:h') . '/index.html') . ' --css ' . shellescape(s:project_root . '/style.css') . ' -V title=""'
		" autocmd BufWritePost *.md execute '!python3 ' . shellescape(expand('<sfile>:p:h') . '/build.py')
endfunction

" autocmd BufWritePost *.md !pandoc -s <afile> -o index.html
" autocmd BufWritePost *.md !pandoc -o index.html <afile>
" autocmd BufWritePost *.md !pandoc -s <afile> -o index.html --css style.css
