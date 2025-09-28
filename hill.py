# hill_cipher_app.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# ----------------- TOÁN HỌC CƠ BẢN -----------------
def mod_inverse(a, m):
    """Tìm nghịch đảo modular của a mod m (Extended Euclidean)"""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None  # nếu không tồn tại

def matrix_inverse_2x2(matrix, mod=26):
    """Tìm ma trận nghịch đảo mod 26 (chỉ hỗ trợ 2x2)"""
    a, b = matrix[0]
    c, d = matrix[1]

    det = (a*d - b*c) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv is None:
        raise ValueError("Ma trận khóa không khả nghịch mod 26!")

    inv_matrix = [
        [( d * det_inv) % mod, (-b * det_inv) % mod],
        [(-c * det_inv) % mod, ( a * det_inv) % mod]
    ]
    return inv_matrix

def mat_vec_mul(matrix, vector):
    return [
        (matrix[0][0]*vector[0] + matrix[0][1]*vector[1]) % 26,
        (matrix[1][0]*vector[0] + matrix[1][1]*vector[1]) % 26
    ]

def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr(n + ord('A'))

# ----------------- HÀM MÃ HÓA & GIẢI MÃ -----------------
def hill_process(text, key_matrix):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'X'  # thêm nếu độ dài lẻ
    
    result_text = ""
    for i in range(0, len(text), 2):
        pair = [char_to_num(text[i]), char_to_num(text[i+1])]
        result = mat_vec_mul(key_matrix, pair)
        result_text += num_to_char(result[0]) + num_to_char(result[1])
    
    return result_text

# ----------------- APP CHÍNH -----------------
def main():
    console.print(Panel("[bold cyan]Hill Cipher App (2x2)[/bold cyan]", expand=False))

    key = [[3, 3],
           [2, 5]]

    # Menu
    console.print("[bold yellow]Chọn chế độ:[/bold yellow]")
    console.print("1. Mã hóa (Encrypt)")
    console.print("2. Giải mã (Decrypt)")
    choice = console.input("[bold green]Nhập lựa chọn (1/2): [/bold green]")

    text = console.input("[bold magenta]Nhập chuỗi: [/bold magenta]")

    if choice == "1":
        result = hill_process(text, key)
        action = "Mã hóa"
    elif choice == "2":
        inv_key = matrix_inverse_2x2(key)
        result = hill_process(text, inv_key)
        action = "Giải mã"
    else:
        console.print("[red]Lựa chọn không hợp lệ![/red]")
        return

    # Hiển thị kết quả bằng bảng
    table = Table(title=f"Kết quả {action}", style="bold blue")
    table.add_column("Chuỗi nhập", justify="center", style="yellow")
    table.add_column(f"Chuỗi {action}", justify="center", style="cyan")

    table.add_row(text.upper(), result)

    console.print(table)

if __name__ == "__main__":
    main()
