param(
    [int]$MaxDepth = 3
)

$ExcludeNames = @('.git', '.venv', '.pytest_cache', '__pycache__', 'node_modules', '.next', 'dist', 'build')

function Show-Tree {
    param(
        [string]$Path,
        [int]$Depth,
        [int]$MaxDepth
    )

    if ($Depth -ge $MaxDepth) { return }

    $dirs = Get-ChildItem -LiteralPath $Path -Directory -Force |
        Where-Object { $ExcludeNames -notcontains $_.Name } |
        Sort-Object Name

    foreach ($d in $dirs) {
        $indent = ' ' * (($Depth + 1) * 2)
        Write-Output ("$indent|-- " + $d.Name)
        Show-Tree -Path $d.FullName -Depth ($Depth + 1) -MaxDepth $MaxDepth
    }
}

$root = (Get-Location).Path
Write-Output $root
Show-Tree -Path $root -Depth 0 -MaxDepth $MaxDepth