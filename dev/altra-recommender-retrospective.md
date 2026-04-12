---
title: "Development | altra-recommender 開発の舞台裏と推薦ロジック 2026"
date: "2026-04-09"
category: "dev"
description: "推薦ロジック、データ構造、結果の見せ方を振り返るレコメンド系 Web アプリの制作記録。"
themes: ["dev:webapp", "dev:algorithm", "other:retrospective"]
---

# Development | altra-recommender 開発の舞台裏と推薦ロジック 2026

## 超要約
本記事は、過去に制作したレコメンドエンジン「altra-recommender」の開発プロセスを振り返ったものです。単なる[アルゴリズム](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="アルゴリズム")の実装にとどまらず、推薦結果の「納得感」や「可読性」といった [UI](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="UI") 体験、および[フロントエンド](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="フロントエンド")とロジックを密結合させないデータ構造の設計について、実務に繋がる学びをまとめています。

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026-04-09</div>

---

過去に制作した **altra-recommender** は、ユーザーごとに合いそうな候補を提示することを意識して作ったレコメンド系の Web アプリです。見た目だけではなく、**「どうやって候補を出すか」** と **「どう見せれば使いやすいか」** の両方を考える必要があり、ロジックと [UI](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="UI") をつなぐ難しさを学べた制作でした。

## 制作背景

一覧をそのまま見せるのではなく、利用者に合わせて情報を絞り込んだり、候補を提案したりする仕組みに興味があり、このアプリに取り組みました。普段使っているサービスでは当たり前に見えるレコメンド機能も、自分で作る側に回ると、データの扱い方、条件分岐、結果の見せ方まで含めて考えることが多くあります。

そのため、この制作では[アルゴリズム](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="アルゴリズム")だけに寄らず、**推薦結果をどう体験として届けるか** を大きなテーマにしていました。

## 制作で意識したこと

### 1. ロジックと UI を分けて考えすぎない

レコメンド機能は、裏側で正しい結果を返せば終わりではありません。ユーザーにとっては、結果がどう並び、何が見えて、次にどう行動できるかまで含めて [UI](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="UI") 体験になります。そのため、推薦ロジックと表示設計を別物にしすぎず、画面上でどう受け取られるかを考えながら実装しました。

### 2. 情報の出し方を整理する

推薦結果が多すぎると、かえって選びづらくなります。そこで、どの情報を先に見せるか、どこまで詳細を出すか、一覧性と理解しやすさのバランスを意識しました。レコメンドは精度だけでなく、**結果の読みやすさ** も重要だと感じました。

### 3. データ構造を意識して実装する

条件分岐や候補の絞り込みを進める中で、データ構造が整理されていないと修正しづらくなる場面が多くありました。そのため、機能追加を見据えて、どこに何の情報を持たせるかを意識するようになりました。これは今の開発にもつながっている学びです。

## 制作を通して学んだこと

この制作で大きかったのは、[フロントエンド](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="フロントエンド")だけでなく、ロジック設計まで含めてアプリ全体を見る視点が身についたことです。特に、推薦結果の質だけを追うのではなく、**ユーザーが結果をどう受け取るか** を考えることで、実装の優先順位や画面設計の考え方が大きく変わりました。

また、レコメンド機能は「何をおすすめするか」だけでなく、「なぜそれが出てきたのか」が見えないと使いにくくなる場面もあります。結果の理由や納得感まで含めて設計する重要性を、この制作で実感しました。

## 今ならこう改善する

もし今作り直すなら、次の点をさらに強化したいです。

1. 推薦の理由を [UI](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="UI") 上で伝え、納得感を高める
2. データ構造とロジックを整理し、保守しやすくする
3. 結果一覧の見せ方を改善し、比較しやすい画面にする

過去制作として振り返ると、altra-recommender は完成度以上に、**少し難しいテーマに自分で踏み込んだこと** に価値があると感じています。挑戦の過程で、[UI](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="UI")、データ、ロジックを横断して考える経験ができたことが、この制作の一番大きな収穫でした。

## リンク

- GitHub: https://github.com/fumiya5222/altra-recommender


## 変更履歴 (Changelog)
- **2026-04-09**: 全体的な標準化アップデート。「Synthetic Edition」デザイン規格に基づき、メタデータの再定義、およびタイトルと日付の同期を実施。
- **2026-04-06**: 用語の自動抽出とクロスリンク（Glossary）の適用、ならびに日付メタデータの統一アップデート、超要約の追加を実施。

