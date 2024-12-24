# MiniLisp Interpreter

此**Final Project**是一個 **MiniLisp Interpreter**，使用 Python 實作，並運用 **Lark** 套件處理 MiniLisp 的語法與執行解析後的抽象語法樹 (AST)。

---

## 功能

- **基本算術運算**：支援加法、減法、乘法、除法與取餘。
- **布林運算**：處理邏輯運算符，例如 `and`、`or` 和 `not`。
- **關係運算**：包含比較運算符，例如 `greater`、`smaller` 和 `equal`。
- **條件語句**：實作 `if-else` 表達式，用於決策。
- **變數定義**：允許在表達式中宣告與使用變數。
- **函數定義與呼叫**：支援用戶自定義函數，包含參數與區域變數。
- **輸入解析**：可從 `.lsp` 檔案中讀取並執行 MiniLisp 程式。
- **錯誤處理**：包含強大的型別檢查與語法錯誤偵測。

---

## 專案結構

### 主要檔案

- **`MiniLisp.py`**：主要的直譯器，用於解析並執行 MiniLisp 程式。
- **`grammar.lark`**：定義 MiniLisp 語法規則的 Lark 文法檔案。
- **`public_test_data/`**：包含範例 `.lsp` 檔案的資料夾，用於測試直譯器。

---

## Quick Start

### 環境需求

- **Python 3.8+**
- **Lark Library**：透過 pip 安裝：
  ```bash
  pip install lark