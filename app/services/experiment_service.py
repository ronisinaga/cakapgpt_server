import asyncio
from app.helpers.StreamWriterHelper import StreamCharOfTextWriter,StreamCharWriter,StreamDoneWriter

async def showExperiment():
    arr_msg = []
    arr_msg.append(f"Terimakasih atas pilihan kamu. Saya akan coba jelaskan mengenai penelitian yang dilakukan oleh pembuat saya Roni Sinag bersama dengan tim kelompok 3")
    arr_msg.append(f"Penelitian ini adalah mengenai analisis sentimen menggunakan metode KLLMs4Rec:Knowledge graph-enhanced LLMs sentiment extraction for personalized recommemdation")
    arr_msg.append(f"Tujuan dari penelitian ini adalah menilai sentiment pengguna IMDB terkait film-film yang bisa ditonton oleh pengguna di website IMDB melalui komentar-komentar yang diberikan oleh pengguna IMDB berkaitan dengan film yang mereka tonton")
    arr_msg.append(f"Seperti yang dijelaskan pada jurnal, ada 4 tahapan yang dilakukan dalam metode KLMMs4Rec:")
    arr_msg.append(f"1. Konstruksi Prompt Template Berbasis Knowledge Graph (KG)")
    arr_msg.append(f"2. Ekstraksi Sentimen Aspek via LLM")
    arr_msg.append(f"3. Propagasi Preferensi (Hierarchical Sentiment Attention GCN)")
    arr_msg.append(f"4. Prediksi dan Pembelajaran (Learning Algorithm)")
    arr_msg.append(f"Sebelum menjelaskan ke-4 tahapan diatas, kita ketahui dulu raw data yang digunakan oleh peneliti dalam jurnal ini. raw data sebagian diambil dari website IMDB dengan alamat url https://datasets.imdbws.com/ dan https://grouplens.org/datasets/movielens/")
    arr_msg.append(f"Raw data yang diambil dari https://datasets.imdbws.com/:")
    arr_msg.append(f"1. title.akas.tsv (2,67 GB)")
    arr_msg.append(f"2. title.crew.tsv (392 MB)")
    arr_msg.append(f"3. title.episode.tsv (241 MB)")
    arr_msg.append(f"4. title.principals.tsv (4,21 GB)")
    arr_msg.append(f"5. title.ratings.tsv (27,4 MB)")
    arr_msg.append(f"6. name.basics.tsv (902,15 MB)")
    arr_msg.append(f"7. title.basics.tsv (1,03 GB)")
    arr_msg.append(f"Raw data yang diambil dari https://grouplens.org/datasets/movielens/:")
    arr_msg.append(f"1. reviews.json (3,83 GB) dengan jumlah objek data ")
    arr_msg.append(f"2. movies_clean.csv (3,4 MB) dengan jumlah objek data")
    arr_msg.append(f"Setelah kita mengetahui besarnya raw data yang diolah maka kita akan lanjut melakukan Langkah demi Langkah yang dilakukan pada metode KLMMs4Rec:")
    arr_msg.append(f"1. Konstruksi Prompt Template Berbasis Knowledge Graph (KG)")
    arr_msg.append(f"Seperti yang diusulkan oleh penulis dalam jurnal, tahapan ini dilakukan secara manual mengingatkan besarnya data yang akan diolah Knowledge Graph yang dibentuk Triplet Knowledge Graph. Triplet Knowledge Graph bentuknya seperti dibawah ini:")
    arr_msg.append("{head,relation,tail}")
    arr_msg.append("contoh: {'head': 'The Story of the Kelly Gang', 'relation': 'Actor', 'tail': 'Sam Crewes'}")
    arr_msg.append("Untuk membentuk Triplet Knowledge Graph, kita harus membentuk komponennya terlebih dahulu:")
    arr_msg.append("1. Membentuk data jsonl (json per line) nama-nama orang terkait suatu film beserta sebagai apa orang tersebut pada film. untuk mendapatkan ini dibuatkan code python ekstrak data dari file name.basics.tsv. Hasilnya adalah name_basics_line.json (453,23 MB). Format objek jsonnya adalah:")
    arr_msg.append("{'nconst': ['nm0000001', 'nm0000002'],primaryName:['Alan Ladd','Veronica Lake']")
    arr_msg.append("2. Membentuk data jsonl (json per line) detail dari film. untuk mendapatkan ini dibuatkan code python ekstrak data dari file title.basics.tsv. Hasilnya adalah name_basics_line.json (1,16 GB). Format objek jsonny adalah:")
    arr_msg.append("{'tconst': ['tt0000001'], 'primaryTitle': ['Carmencita'], 'genres': ['Documentary', 'Short']}")
    arr_msg.append("3. Membentuk data jsonl (json per line) detail dari kru2 film. untuk mendapatkan ini dibuatkan code python ekstrak data dari file title.principals.tsv. Hasilnya adalah name_basics_line.json (3,95 GB). Format objek jsonny adalah:")
    arr_msg.append("{'tconst': ['tt0000001', 'tt0000001', 'tt0000001', 'tt0000001'], 'nconst': ['nm1588970', 'nm0005690', 'nm0005690', 'nm0374658'], 'category': ['self', 'director', 'producer', 'cinematographer']}")
    arr_msg.append("Setelah kita membentuk komponen pembentuk Triplet Knowledge Graph nya maka kita akan membentuk Triplet Knowledge Graph nya dengan format:")
    arr_msg.append("{'head': 'The Story of the Kelly Gang', 'relation': 'Actor', 'tail': 'Sam Crewes'}")
    arr_msg.append("Pembentukan ini menghasilkan file kg_triples.json (1,9 GB)")
    arr_msg.append("Langkah selanjutnya adalah membentuk data menggabungkan data film (movie_clean.csv) dengan data review (reviews.json). pembentukan data akan menghasilkan file moview_reviews.jsonl (3,9 GB). Formatnya objek jsonnya adalah:")
    arr_msg.append("{'item_id':7065,'movie':'Birth of a Nation, The','txt':'unbelievable; I cannot understand how anyone can call this one of the greatest movies ever made. It is disgraceful and appalling. I guess it is still high entertainment to see white actors in black face and watch a film loaded with stereotype.'}")
    arr_msg.append("Langkah selanjutnya adalah membentuk prompt yang siap dikirimkan ke AI seperti Gemini, ChatGPT dan lainnya. Sebelum dibentuk prompt ini maka Langkah selanjutnya adalah mengubah Triplet Knowledge Group untuk kepentingan prompt dengan format:")
    arr_msg.append("{'head': 'Carmencita', 'relation': 'Genre', 'tail': ['Action', 'Adult', 'Animation', 'Documentary', 'Drama', 'Short']}")
    arr_msg.append("Setelah itu digabungkan movie_reviews.json untuk membentuk prompt yang siap dikirimkan ke Gemini sebagai contohnya. Gabungan dari data ini akan membentuk prompt dengan format:")
    arr_msg.append("{'item_id': 7458, 'movie': 'Troy', 'relation': 'Actor', 'tail': ['Max Jenkins'], 'txt': 'Not much new here ... just a remake; What bothers me the most about this epic is that an entire war was fought over a woman. Will men ever learn that \"she\" is not worth it? She is not worth it at all. Aside from that... This is just a remake. Different actors, better special effects, and better costumes. But this is still just a remake. Hollywood needs to do something new. And why do movies like these always seem to be released in pairs? Troy and Alexander. The two movies about volcanoes. The two movies about asteroids. It was fine as a rental (it breaks the monotony of TV), and I'm glad that I didn't spend my money to see it in the theaters. I would never buy it.'}")
    arr_msg.append("2. Ekstraksi Sentimen Aspek via LLM")
    arr_msg.append("Langkah kedua ari metode KLLMs4Rec adalah mengekstrak response sentimen dari prompt yang kita kirim")
    arr_msg.append("Peneliti menmberikan format penilaian dari respon LLM adalah [1 0 -1], dimana 1 responnya positif, -1 responnya negative dan 0 responnya netral")
    arr_msg.append("Namun sayangnya, proses ini tidak berhasil dilakukan karena keterbatasan penggunaan LLM (Gemini, ChatGPT) harian. salah satu pesan errornya adalah: ")
    arr_msg.append("Error saat menghubungi Gemini: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit.")
    arr_msg.append("Namun ada sedikit hasil dari collab sebelum collab pun gagal mendapatkan data")
    arr_msg.append("{'item_id': 5219, 'movie': 'Resident Evil', 'relation': 'Director', 'tail': ['T.C. De Witt'], 'txt': 'awful; I saw the movie for the first time last night, and I was really looking forward to it. When I sat down to watch it I thought, this is so cool, especially when all the gas comes through the vents and the people die. Then it went from bad to worse. The story was very bland, and the zombies weren't even scary at all.The acting was so bad it was funny. The game was more scary. This was a complete flop. I felt as if there was pieces missing from the movie. Acting bad, props bad, and what was Milla Jovovich (Alice) costume all about? It was AWFUL. The only part I did like was the Queen. She seemed to be helping everyone, even though she was supposed to be bad. One of the worst movies I have honestly ever seen. D- all round.', 'sentiment_vector': [-1]}")
    for message in arr_msg:
        for word in message.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
    await asyncio.sleep(1)
    yield "[DONE]"