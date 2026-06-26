# Rebrand global de tokens ASCII (sem acento) — Gomes & Dutra
$ErrorActionPreference = 'Stop'
$root = 'C:\Users\gabri\GomesEDutra'

# pares ordenados (mais especifico primeiro). Apenas valores ASCII.
$pairs = @(
  @('logo-exemplo.png',        'logo-gd.png'),
  @('seal-exemplo.png',        'seal-gd.png'),
  @('favicon-exemplo.png',     'favicon-gd.png'),
  @('5500000000000',           '5533999547938'),
  @('(00) 00000-0000',         '(33) 99954-7938'),
  @('contato@seudominio.com.br','escritoriogomesedutra@gmail.com'),
  @('/SeuSiteExemplo/',        '/GomesEDutra/'),
  @('SeuSiteExemplo',          'GomesEDutra'),
  @('Nome Sobrenome Advocacia','Gomes & Dutra Advocacia'),
  @('Nome Sobrenome',          'Gomes & Dutra'),
  @('Ol%C3%A1%2C%20Nome',      'Ol%C3%A1%2C%20Gomes%20%26%20Dutra')
)

$files = @(
  'index.html',
  '_layouts\base.html',
  '_layouts\landing.html',
  'scripts\build_site.py',
  'assets\content-loader.js',
  'assets\site-config.json',
  'README.md'
)

$enc = New-Object System.Text.UTF8Encoding($false)
foreach ($rel in $files) {
  $path = Join-Path $root $rel
  if (-not (Test-Path $path)) { Write-Output "SKIP (nao existe): $rel"; continue }
  $txt = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
  foreach ($p in $pairs) { $txt = $txt.Replace($p[0], $p[1]) }
  [System.IO.File]::WriteAllText($path, $txt, $enc)
  Write-Output "OK: $rel"
}
Write-Output 'Rebrand concluido.'
