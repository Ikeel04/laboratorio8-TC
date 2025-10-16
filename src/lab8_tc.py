import argparse
import os
import time
import csv
import matplotlib
matplotlib.use("Agg")  # backend no interactivo para PNGs
import matplotlib.pyplot as plt


def problem1(n: int) -> int:
    """
    Programa del Problema 1: cuenta cuántas veces ejecuta counter++.
    i: n/2 .. n
    j: 1 .. (j + n/2 <= n)  -> j <= n - floor(n/2)
    k: 1; k*=2 hasta n
    """
    counter = 0
    i = n // 2
    while i <= n:
        j = 1
        while j + n // 2 <= n:
            k = 1
            while k <= n:
                counter += 1
                k *= 2
            j += 1
        i += 1
    return counter


def problem2(n: int) -> int:
    """
    Programa del Problema 2: el break hace que se imprima 1 vez por i.
    """
    if n <= 1:
        return 0
    cnt = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            cnt += 1
            break
    return cnt


def problem3(n: int) -> int:
    """
    Programa del Problema 3: i = 1..n/3, j = 1..n paso 4.
    """
    cnt = 0
    for i in range(1, n // 3 + 1):
        j = 1
        while j <= n:
            cnt += 1
            j += 4
    return cnt


def time_function(func, n: int, repeat: int = 1):
    """
    Mide tiempo mínimo de repeat ejecuciones y devuelve (t_min, resultado).
    """
    best = float("inf")
    result = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        result = func(n)
        t1 = time.perf_counter()
        best = min(best, t1 - t0)
    return best, result


def ensure_outputs_dir(script_dir: str) -> str:
    out_dir = os.path.abspath(os.path.join(script_dir, "..", "outputs"))
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def write_csv(path, rows, header=("n", "time_seconds", "ops_count", "note")):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow([r.get(h) for h in header])


def plot_series(path_png, rows, title):
    measured = [r for r in rows if r.get("time_seconds") is not None]
    if not measured:
        return
    xs = [r["n"] for r in measured]
    ys = [r["time_seconds"] for r in measured]
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.xlabel("Tamaño de entrada n")
    plt.ylabel("Tiempo (s)")
    plt.title(title)
    plt.xscale("log")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig(path_png, bbox_inches="tight")
    plt.close()


def do_profile(Ns, script_dir):
    out_dir = ensure_outputs_dir(script_dir)
    limits = {"p1": 1000, "p2": 1_000_000, "p3": 10000}

    # P1
    rows_p1 = []
    for n in Ns:
        if n <= limits["p1"]:
            t, cnt = time_function(problem1, n, repeat=1)
            rows_p1.append({"n": n, "time_seconds": t, "ops_count": cnt, "note": ""})
        else:
            rows_p1.append({"n": n, "time_seconds": None, "ops_count": None,
                            "note": "Demasiado costoso (O(n^2 log n))."})
    write_csv(os.path.join(out_dir, "profiling_p1.csv"), rows_p1)
    plot_series(os.path.join(out_dir, "profiling_p1.png"), rows_p1,
                "Problema 1: n vs tiempo (medido)")

    # P2
    rows_p2 = []
    for n in Ns:
        if n <= limits["p2"]:
            t, cnt = time_function(problem2, n, repeat=3)
            rows_p2.append({"n": n, "time_seconds": t, "ops_count": cnt, "note": ""})
        else:
            rows_p2.append({"n": n, "time_seconds": None, "ops_count": None,
                            "note": "Fuera de rango (seguridad)."})
    write_csv(os.path.join(out_dir, "profiling_p2.csv"), rows_p2)
    plot_series(os.path.join(out_dir, "profiling_p2.png"), rows_p2,
                "Problema 2: n vs tiempo (medido)")

    # P3
    rows_p3 = []
    for n in Ns:
        if n <= limits["p3"]:
            t, cnt = time_function(problem3, n, repeat=1)
            rows_p3.append({"n": n, "time_seconds": t, "ops_count": cnt, "note": ""})
        else:
            rows_p3.append({"n": n, "time_seconds": None, "ops_count": None,
                            "note": "Demasiado costoso (O(n^2))."})
    write_csv(os.path.join(out_dir, "profiling_p3.csv"), rows_p3)
    plot_series(os.path.join(out_dir, "profiling_p3.png"), rows_p3,
                "Problema 3: n vs tiempo (medido)")

    print("[OK] CSVs y PNGs generados en:", out_dir)


def main():
    ap = argparse.ArgumentParser(description="Lab 8 TC — Ejecución y perfilado")
    ap.add_argument("--profile", action="store_true",
                    help="Genera CSVs y gráficas.")
    ap.add_argument(
        "--nlist",
        type=str,
        default="1,10,100,1000,10000,100000,1000000",
        help="Lista de n separados por coma."
    )
    args = ap.parse_args()

    Ns = []
    for tok in args.nlist.split(","):
        tok = tok.strip()
        if tok:
            Ns.append(int(tok))

    script_dir = os.path.dirname(os.path.abspath(__file__))

    for n in [x for x in Ns if x <= 1000][:4]:
        for idx, func in enumerate([problem1, problem2, problem3], start=1):
            t, res = time_function(func, n, repeat=1)
            print(f"Problema {idx}, n={n} -> tiempo={t:.6f}s, cuenta={res}")

    if args.profile:
        do_profile(Ns, script_dir)


if __name__ == "__main__":
    main()
