import threading
import multiprocessing
import time


def ogir_hisob(n):
    print(f"  [Process] {n}-hisob boshlandi")
    natija = sum(i * i for i in range(5_000_000))
    print(f"  [Process] {n}-hisob tugadi")
    return natija


def qayta_ishla(data):
    return f"{data}_QAYTA_ISHLANDI"


def multithreading_misol():
    print("\n" + "=" * 50)
    print("MULTITHREADING")
    print("=" * 50)

    urllar = ["https://site1.com", "https://site2.com",
              "https://site3.com", "https://site4.com"]

    natijalar = [None] * len(urllar)
    lock = threading.Lock()
    threadlar = []
    boshlanish = time.time()

    def yukla(url, index):
        print(f"  [Thread] Boshlanmoqda: {url}")
        time.sleep(2)
        with lock:
            natijalar[index] = f"{url} → yuklandi"
        print(f"  [Thread] Tugadi: {url}")

    for i, url in enumerate(urllar):
        t = threading.Thread(target=yukla, args=(url, i))
        threadlar.append(t)
        t.start()

    for t in threadlar:
        t.join()

    print(f"Natijalar: {natijalar}")
    print(f"Vaqt: {time.time() - boshlanish:.2f} soniya")


def multiprocessing_misol():
    print("\n" + "=" * 50)
    print("MULTIPROCESSING")
    print("=" * 50)

    cpu_soni = multiprocessing.cpu_count()
    print(f"CPU core soni: {cpu_soni}")
    boshlanish = time.time()

    with multiprocessing.Pool(processes=cpu_soni) as pool:
        natijalar = pool.map(ogir_hisob, [1, 2, 3, 4])

    print(f"Natijalar: {natijalar}")
    print(f"Vaqt: {time.time() - boshlanish:.2f} soniya")


def birga_ishlatish():
    print("\n" + "=" * 50)
    print("IKKALASI BIRGA")
    print("=" * 50)

    yuklanganlar = []
    lock = threading.Lock()

    def yukla(nom):
        time.sleep(1)
        with lock:
            yuklanganlar.append(f"data_{nom}")

    threadlar = [threading.Thread(target=yukla, args=(i,)) for i in range(4)]
    for t in threadlar:
        t.start()
    for t in threadlar:
        t.join()

    print(f"Yuklangan: {yuklanganlar}")

    with multiprocessing.Pool(processes=2) as pool:
        natijalar = pool.map(qayta_ishla, yuklanganlar)

    print(f"Qayta ishlangan: {natijalar}")
    print("Muvaffaqiyatli tugadi!")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    multithreading_misol()
    multiprocessing_misol()
    birga_ishlatish()