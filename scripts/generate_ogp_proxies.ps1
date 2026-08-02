# generate_ogp_proxies.ps1
# Generates OGP proxy HTML files, article_index.json, article-data.js, and skill-data.js

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$rootDir = Get-Item .
$srcDir = Join-Path $rootDir.FullName "md"
$outDir = Join-Path $rootDir.FullName "html"
$jsonOutPath = Join-Path $rootDir.FullName "assets\data\article_index.json"
$jsArticlePath = Join-Path $rootDir.FullName "assets\js\article-data.js"
$jsSkillPath = Join-Path $rootDir.FullName "assets\js\skill-data.js"
$skillMdPath = Join-Path $rootDir.FullName "SKILL.md"

if (-not (Test-Path $srcDir)) {
    Write-Error "Source directory 'md' not found."
    exit 1
}

$articlesIndex = @()
$count = 0

$mdFiles = Get-ChildItem -Path $srcDir -Recurse -Filter "*.md"

foreach ($file in $mdFiles) {
    $relPath = $file.FullName.Substring($srcDir.Length + 1).Replace('\', '/')
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    
    # Parse frontmatter
    $title = ""
    $description = ""
    $date = "2026-08-02"
    $updated = "2026-08-02"
    
    if ($content.StartsWith("---")) {
        $parts = $content.Split("---")
        if ($parts.Count -ge 3) {
            $fmLines = $parts[1].Split("`n")
            foreach ($rawLine in $fmLines) {
                $line = $rawLine.Trim()
                if ($line -match '^title:\s*(.*)$') {
                    $title = $Matches[1].Trim().Trim('"').Trim("'")
                }
                elseif ($line -match '^description:\s*(.*)$') {
                    $description = $Matches[1].Trim().Trim('"').Trim("'")
                }
                elseif ($line -match '^date:\s*(.*)$') {
                    $date = $Matches[1].Trim().Trim('"').Trim("'")
                }
                elseif ($line -match '^updated:\s*(.*)$') {
                    $updated = $Matches[1].Trim().Trim('"').Trim("'")
                }
            }
        }
    }
    
    if ([string]::IsNullOrWhiteSpace($title)) {
        if ($content -match "(?m)^#\s+(.+)$") {
            $title = $Matches[1].Trim()
        } else {
            $title = $file.BaseName
        }
    }

    if ([string]::IsNullOrWhiteSpace($description)) {
        $description = "$title - FunUni-lab Technical Archive"
    }
    
    $htmlRelPath = $relPath -replace '\.md$', '.html'
    $outPath = Join-Path $outDir ($htmlRelPath.Replace('/', '\'))
    
    $outParent = Split-Path -Parent $outPath
    if (-not (Test-Path $outParent)) {
        New-Item -ItemType Directory -Path $outParent -Force | Out-Null
    }
    
    $depth = ($htmlRelPath -split '/').Length - 1
    $relRoot = "../" * ($depth + 1)
    
    $template = @"
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO & OGP -->
    <title>$title | FunUni-lab</title>
    <meta name="description" content="$description" />
    <meta property="og:title" content="$title | FunUni-lab" />
    <meta property="og:description" content="$description" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="https://fununi222.github.io/website/html/$htmlRelPath" />
    <meta property="og:site_name" content="FunUni-lab" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="$title | FunUni-lab" />
    <meta name="twitter:description" content="$description" />
    <link rel="canonical" href="https://fununi222.github.io/website/html/$htmlRelPath" />
    <meta http-equiv="refresh" content="0;url=${relRoot}article.html?md=md/$relPath">

    <!-- Redirect to the dynamic viewer -->
    <script>
        window.location.href = '${relRoot}article.html?md=md/$relPath';
    </script>
    
    <style>
        body { background: #0f172a; color: #a3aac4; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .loading { text-align: center; }
        .spinner { border: 2px solid rgba(255,255,255,0.1); border-left-color: #aaa4ff; border-radius: 50%; width: 20px; height: 20px; animation: spin 1s linear infinite; margin: 0 auto 10px; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="loading">
        <div class="spinner"></div>
        <p>Redirecting to Research Log...</p>
    </div>
</body>
</html>
"@
    
    [System.IO.File]::WriteAllText($outPath, $template, [System.Text.Encoding]::UTF8)
    
    $category = if ($relPath.Contains('/')) { $relPath.Split('/')[0] } else { 'other' }
    
    $articlesIndex += [PSCustomObject]@{
        title = $title
        description = $description
        date = $date
        updated = $updated
        category = $category
        path = $htmlRelPath
    }
    
    $count++
}

# Sort descending by date, updated
$articlesIndex = $articlesIndex | Sort-Object -Property @{Expression="date"; Descending=$true}, @{Expression="updated"; Descending=$true}

# Convert to JSON
$jsonContent = ($articlesIndex | ConvertTo-Json -Depth 10).Replace("\u0026", "&")

$jsonDir = Split-Path -Parent $jsonOutPath
if (-not (Test-Path $jsonDir)) { New-Item -ItemType Directory -Path $jsonDir -Force | Out-Null }
[System.IO.File]::WriteAllText($jsonOutPath, $jsonContent, [System.Text.Encoding]::UTF8)
Write-Host " [CREATED] $jsonOutPath with $($articlesIndex.Count) entries."

# Generate article-data.js
$jsArticleContent = "const window_article_index = $jsonContent;"
[System.IO.File]::WriteAllText($jsArticlePath, $jsArticleContent, [System.Text.Encoding]::UTF8)
Write-Host " [CREATED] $jsArticlePath with $($articlesIndex.Count) entries."

# Extract skill data from SKILL.md
if (Test-Path $skillMdPath) {
    $skillContent = [System.IO.File]::ReadAllText($skillMdPath, [System.Text.Encoding]::UTF8)
    $skillMap = [ordered]@{}
    $lines = $skillContent -split "`n"
    foreach ($l in $lines) {
        if ($l -match '^\s*-\s*\*\*([^:*]+)\*\*:\s*(\d+)') {
            $key = $Matches[1].Trim() -replace '\[([^\]]+)\]\([^)]+\)', '$1'
            $val = [int]$Matches[2]
            $skillMap[$key] = $val
        }
    }
    $skillJson = $skillMap | ConvertTo-Json
    $jsSkillContent = "const window_skill_data = $skillJson;"
    [System.IO.File]::WriteAllText($jsSkillPath, $jsSkillContent, [System.Text.Encoding]::UTF8)
    Write-Host " [CREATED] $jsSkillPath with $($skillMap.Count) skills."
}

Write-Host "`nDone! Successfully processed $count markdown and HTML files."
