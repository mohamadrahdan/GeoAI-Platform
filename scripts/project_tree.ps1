$root = Get-Location
$exclude = '\\.venv\\|\\.git\\|__pycache__|\\.pytest_cache\\'

Write-Host $root.Path

Get-ChildItem -Path $root -Recurse -Directory -Force |
Where-Object { $_.FullName -notmatch $exclude } |
Sort-Object FullName |
ForEach-Object {
    $depth = ($_.FullName -split '\\').Count - ($root.Path -split '\\').Count
    (' ' * ($depth * 2)) + '|-- ' + $_.Name
}