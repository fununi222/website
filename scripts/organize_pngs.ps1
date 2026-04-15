param()

$workspace = "c:\Users\fumiy\.openclaw\workspace\website"
$imgDir = "$workspace\assets\img"
$categories = @("ai", "infra", "dev", "finance", "lpo", "other")

foreach ($cat in $categories) {
    $catPath = "$imgDir\$cat"
    if (-not (Test-Path $catPath)) {
        New-Item -ItemType Directory -Path $catPath | Out-Null
    }
}

$pngs = Get-ChildItem -Path $imgDir -File -Filter *.png

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$textFiles = Get-ChildItem -Path $workspace -Include *.md,*.html,*.js -Recurse | Where-Object { -not $_.DirectoryName.Contains(".git") -and -not $_.DirectoryName.Contains("node_modules") }

foreach ($png in $pngs) {
    if ($categories -contains $png.Directory.Name) {
        continue # Already in a category folder somehow
    }

    $targetCat = $null
    
    # Check 1: Does it match an article name exactly within a category?
    foreach ($cat in $categories) {
        $mdPath = "$workspace\$cat\$($png.BaseName).md"
        if (Test-Path $mdPath) {
            $targetCat = $cat
            break
        }
    }
    
    # Check 2: If no exact match, try to deduce from its usages across text files
    if ($targetCat -eq $null) {
        $referencedInCats = @()
        foreach ($tf in $textFiles) {
            $content = Get-Content $tf.FullName -Raw
            if ($content -ne $null -and $content.Contains("assets/img/$($png.Name)")) {
                $parentDir = (Split-Path $tf.DirectoryName -Leaf)
                if ($categories -contains $parentDir) {
                    $referencedInCats += $parentDir
                }
            }
        }
        $referencedInCats = $referencedInCats | Select-Object -Unique
        if ($referencedInCats.Length -eq 1) {
            $targetCat = $referencedInCats[0]
        }
    }
    
    # Perform move and regex replacement
    if ($targetCat -ne $null) {
        $catDir = "$imgDir\$targetCat"
        Move-Item -Path $png.FullName -Destination "$catDir\$($png.Name)" -Force
        
        foreach ($tf in $textFiles) {
            $content = Get-Content $tf.FullName -Raw
            if ($content -ne $null -and $content.Contains("assets/img/$($png.Name)")) {
                $escapedName = [regex]::Escape($png.Name)
                $newContent = $content -replace "assets/img/$escapedName", "assets/img/$targetCat/$($png.Name)"
                [System.IO.File]::WriteAllText($tf.FullName, $newContent, $utf8NoBom)
            }
        }
        Write-Host "Moved $($png.Name) to $targetCat and updated references"
    } else {
        Write-Host "Skipped $($png.Name) (matches multiple categories or root files only)"
    }
}
Write-Host "Organization complete!"
