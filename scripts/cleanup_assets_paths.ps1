param()
$workspace = "c:\Users\fumiy\.openclaw\workspace\website"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# 1. 漏れている特殊名・派生名画像の移動とパス更新
$manualMoves = @{
    "aws-rds-tech-deep-dive-2026.png" = "infra"
    "mascot-happy.png" = "dev"
    "mascot-idle.png" = "dev"
    "mascot-sad.png" = "dev"
    "mascot-sleep.png" = "dev"
    "mascot-v3-happy.png" = "dev"
    "mascot-v3-idle.png" = "dev"
    "mascot-v3-sad.png" = "dev"
    "mascot-v3-sleep.png" = "dev"
    "niseko-altra-guide.png" = "other"
    "pet-bg-spring.png" = "dev"
    "zushi-yamanone-railway-view.png" = "other"
    "zushi-yamanone-railway-zoom.png" = "other"
    "zushi-yamanone-sanjinja-close.png" = "other"
    "zushi-yamanone-sanjinja-torii.png" = "other"
    "zushi-yamanone-shrine-flowers.png" = "other"
    "zushi-yamanone-strata-detail.png" = "other"
    "zushi-yamanone-torii.png" = "other"
    "zushi-yamanone-yagura-cave.png" = "other"
}

foreach ($item in $manualMoves.GetEnumerator()) {
    $src = "$workspace\assets\img\$($item.Key)"
    $dest = "$workspace\assets\img\$($item.Value)\$($item.Key)"
    if (Test-Path $src) {
        if (-not (Test-Path "$workspace\assets\img\$($item.Value)")) {
            New-Item -ItemType Directory -Path "$workspace\assets\img\$($item.Value)" | Out-Null
        }
        Move-Item -Path $src -Destination $dest -Force
        
        $textFiles = Get-ChildItem -Path $workspace -Include *.md,*.html,*.js -Recurse | Where-Object { -not $_.DirectoryName.Contains(".git") -and -not $_.DirectoryName.Contains("node_modules") }
        foreach ($tf in $textFiles) {
            $content = Get-Content $tf.FullName -Raw
            $escKey = [regex]::Escape("assets/img/" + $item.Key)
            if ($content -match $escKey) {
                $newContent = $content -replace $escKey, "assets/img/$($item.Value)/$($item.Key)"
                [System.IO.File]::WriteAllText($tf.FullName, $newContent, $utf8NoBom)
                Write-Host "Updated $($item.Key) in $($tf.Name)"
            }
        }
    }
}

# 2. サブディレクトリ上のファイルにおける相対パス `../assets/img/` の適正化補完
$subdirs = @("ai", "infra", "dev", "finance", "lpo", "other", "references", "glossary")
foreach ($dir in $subdirs) {
    if (Test-Path "$workspace\$dir") {
        $mdFiles = Get-ChildItem -Path "$workspace\$dir" -Include *.md,*.html -Recurse
        foreach ($md in $mdFiles) {
            $content = Get-Content $md.FullName -Raw
            if ($content -ne $null -and $content -match "(?<!\.\./|/)assets/img/") {
                $newContent = [regex]::Replace($content, "(?<!\.\./|/)assets/img/", "../assets/img/")
                [System.IO.File]::WriteAllText($md.FullName, $newContent, $utf8NoBom)
                Write-Host "Fixed relative path suffix (prepended ../) in $($md.Name)"
            }
        }
    }
}
Write-Host "Manual cleanup and relative path fix complete!"
