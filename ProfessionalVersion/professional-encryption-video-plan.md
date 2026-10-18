# Professional Encryption Video: Manim Plan

Oct 18, 2026 · @Chris Mobley

## At a glance

The part of the script we have (How Encryption Works, Types, Applications) runs about **8:00**. That leaves 0:30–2:00 for the history intro, which is still being written, to land the full video at 8–10 minutes. The whole video is animated in [Manim Community Edition](https://github.com/ManimCommunity/manim), with no AI-generated video.

|  | Plan |
| --- | --- |
| Runtime | \~8:00 for this portion, plus 0:30–2:00 intro = 8:30–10:00 total |
| Source | 100% Manim (plus narration and background music) |
| Structure | Intro placeholder + 13 scenes in 3 chapters, 77 narrated beats (one per sentence or phrase) |
| Pacing assumption | \~2.5 spoken words per second (\~150 words per minute), a measured technical delivery, plus \~1 second per scene transition |
| Timecodes | Start at 0:00 for this portion. Once the intro exists, add its length to every time. |
| Audience level | Technical: real algorithm names, real AES and SHA-256 output, key sizes, accurate HTTPS flow |

**Runtime by chapter**

| Chapter | Scenes | Time | Length |
| --- | --- | --- | --- |
| Intro: history and evolution *(script pending)* | — | before 0:00 | 0:30–2:00 |
| 1. How Encryption Works | 1–6 | 0:00–2:22 | 2:22 |
| 2. Types of Encryption | 7–10 | 2:22–5:25 | 3:03 |
| 3. Applications of Encryption | 11–13 | 5:25–8:00 | 2:35 |

**Visual style.** Same look as the simplified video so the two feel like a set: flat, geometric, 3Blue1Brown-like, dark navy background (#14213D), thick clean outlines, no gradients. A small chapter tag sits in the top corner throughout, so viewers always know where they are in the 8+ minutes.

| Meaning | Color | Hex |
| --- | --- | --- |
| Plaintext (readable) | Green | #3DDC97 |
| Ciphertext (scrambled) | Red-orange | #FF6B4A |
| Private / shared secret / session key | Gold | #FFC93C |
| Public key | Light blue | #5BC0EB |
| Algorithm / process | Blue | #3A86FF |
| Attacker (Eve) / observers | Gray | #8D99AE |
| Labels and text | Off-white | #F1FAEE |

The recurring cast: **Maya** (sender), **Sam** (recipient) and **Eve** (attacker), all simple circle-head figures built from basic Manim shapes.

## Narration

The group's script is used **word for word** (about 1,060 spoken words). It only needed to be split into beats, not rewritten. The section headings become on-screen chapter cards instead of being read aloud, which saves time and gives viewers a visual reset every 2–3 minutes.

**Two optional accuracy tweaks for a technical audience:**

- **Scene 9:** "help the browser and the server authenticate each other" → "help the browser verify the server's identity". Most HTTPS connections authenticate only the server; client certificates are optional and uncommon. The animation shows the server-only version either way.
- **Scene 13:** No change needed, but expect the question: the classic "CIA triad" is confidentiality, integrity and **availability**. The script lists what encryption itself supports, which is accurate as written.

> **\[Intro\] History and evolution.** *Script pending. Budget 0:30–2:00.*
>
> **\[1. Bridge from the intro\]** Now that we have looked at the history and evolution of encryption, we can examine how encryption works, the major types of encryption, and how encryption is used in modern technology.
>
> ***Chapter 1: How Encryption Works*** *(shown as a chapter card, not read aloud)*
>
> **\[2. Plaintext and ciphertext\]** At its most basic level, encryption is the process of transforming readable information into an unreadable format so that unauthorized people cannot understand it. The original readable information is called plaintext. Encryption uses a mathematical algorithm and a key to transform the plaintext into ciphertext. Ciphertext may look like a random sequence of letters, numbers, or symbols. Although the ciphertext still contains the original information, it is designed to be meaningless to anyone who does not have the correct key.
>
> **\[3. Decryption\]** The intended recipient can then use a key and a decryption algorithm to convert the ciphertext back into plaintext. This process is called decryption.
>
> **\[4. Locked-box analogy\]** A simple analogy is a locked box. The plaintext is the message placed inside the box. The encryption algorithm is the locking mechanism, and the key is what allows the box to be opened. Anyone might be able to see the locked box, but only someone with the correct key should be able to access the message.
>
> **\[5. Mathematics, not hiding\]** Modern encryption is based on mathematics rather than simply hiding information. Algorithms are designed so that encrypting information is easy when the correct key is available, but reversing the process without the key is computationally impractical.
>
> **\[6. What makes encryption strong\]** The strength of encryption depends on several factors. These include the quality of the algorithm, the length and randomness of the key, and how securely the key is stored. Even a strong algorithm can be compromised if a key is stolen, guessed, or accidentally exposed. For example, if an attacker obtains a password used to protect an encrypted file, the encryption itself may not be broken. Instead, the attacker has obtained the key needed to unlock the information. This is why key management is one of the most important parts of cybersecurity.
>
> ***Chapter 2: Types of Encryption*** *(shown as a chapter card, not read aloud)*
>
> **\[7. Symmetric encryption\]** There are two major categories of encryption: symmetric encryption and asymmetric encryption. Symmetric encryption uses the same key for both encryption and decryption. The sender uses the key to encrypt the message, and the recipient uses that same key to decrypt it. Symmetric encryption is generally fast and efficient, which makes it useful for encrypting large amounts of data. Common symmetric encryption algorithms include the Advanced Encryption Standard, or AES, and ChaCha20. However, symmetric encryption creates an important challenge: both parties need to obtain the same secret key securely. If the key is sent through an insecure channel and intercepted, an attacker may be able to decrypt the communication.
>
> **\[8. Asymmetric encryption\]** Asymmetric encryption, also called public-key encryption, uses a pair of mathematically related keys: a public key and a private key. The public key can be shared openly. The private key must be kept secret. Information encrypted with the public key can generally be decrypted only with the corresponding private key. For example, if someone wants to send a secure message to a recipient, they can encrypt the message using the recipient’s public key. Only the recipient’s private key should be able to decrypt it. Asymmetric encryption solves much of the key-distribution problem because the public key does not need to be kept secret. However, it is typically slower and more computationally expensive than symmetric encryption. Examples of public-key algorithms include RSA and elliptic-curve cryptography, often called ECC. ECC can provide strong security with shorter key sizes, which makes it useful in mobile devices, web browsers, and other systems with limited resources.
>
> **\[9. Hybrid encryption and HTTPS\]** In practice, many modern systems use a hybrid approach that combines both types. For example, when a user visits a website using HTTPS, asymmetric cryptography can help the browser and the server authenticate each other and establish a shared session key. After that, symmetric encryption is usually used to protect the actual data exchanged during the session because it is faster. This combination provides both secure key exchange and efficient communication.
>
> **\[10. Hashing and digital signatures\]** It is also important to distinguish encryption from hashing. Hashing transforms data into a fixed-length value, called a hash, but it is not designed to be reversed. Hashing is commonly used to store passwords securely and to verify whether data has been changed. Digital signatures are related to public-key cryptography as well, but they serve a different purpose. Encryption is mainly used to protect confidentiality, while digital signatures help verify the identity of the sender and confirm that the message has not been modified.
>
> ***Chapter 3: Applications of Encryption*** *(shown as a chapter card, not read aloud)*
>
> **\[11. Web, messaging and storage\]** Encryption is used throughout everyday computing. One of the most familiar examples is HTTPS, which protects communication between a web browser and a website. When a website uses HTTPS, information such as login credentials, personal details, and payment information is encrypted while traveling across the internet. Encryption is also used in messaging applications. End-to-end encryption is designed so that a message is encrypted on the sender’s device and decrypted only on the recipient’s device. Ideally, even the messaging provider cannot read the contents of the message while it is in transit. Another major application is data storage. Computers, smartphones, USB drives, and cloud services can encrypt stored files. This is called encryption at rest. If a device is lost or stolen, encryption can make it much more difficult for someone to access the information stored on it.
>
> **\[12. Banking, VPNs and organizations\]** Encryption is also important in online banking and electronic payments. Financial institutions use cryptographic protocols to protect account information, verify transactions, and reduce the risk of unauthorized access. Virtual private networks, or VPNs, use encryption to protect data traveling between a device and a VPN server. This can help prevent people on the same network from easily viewing the user’s traffic. Businesses and governments use encryption to protect confidential records, intellectual property, medical data, and classified information. In these environments, encryption is often combined with access controls, authentication, monitoring, and other security measures.
>
> **\[13. Limits and conclusion\]** However, encryption does not solve every security problem. It cannot protect data from a person who already has authorized access, and it cannot prevent every type of malware, phishing attack, or social-engineering attack. Encryption protects information, but the surrounding systems and users must also be secure. Overall, encryption supports three major security goals: confidentiality, integrity, and authentication. It helps keep information private, helps detect unauthorized changes, and can help verify the identity of the people or systems involved. As more communication, commerce, and personal activity move online, encryption has become a fundamental part of modern computer science and cybersecurity.

## Scene plan

Each row is one beat: the words spoken in that window and what Manim shows while they are spoken. Times assume \~2.5 words per second, with a little extra on list sentences so each item gets its own visual. Times start at 0:00 for this portion; add the intro's length once it's written. Re-time after recording the real narration; the order of beats stays the same.

### Intro: history and evolution (before 0:00)

*Script pending, budget 0:30–2:00.* End the intro on a horizontal history timeline (for example Caesar cipher → Enigma → DES → AES), because Scene 1 opens by compressing that timeline.

**Chapter 1: How Encryption Works (0:00–2:22)**

### 1. Bridge from the intro (0:00–0:14)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:00–0:05 | "Now that we have looked at the history and evolution of encryption," | The intro's history timeline (Caesar cipher → Enigma → DES → AES) compresses into a thin line and slides off to the left. |
| 0:05–0:13 | "we can examine how encryption works, the major types of encryption, and how encryption is used in modern technology." | Three chapter cards slide in, one per phrase: **1 How it works**, **2 Types**, **3 Applications**. |
| 0:13–0:14 | *(transition)* | Cards 2 and 3 dim; card 1 grows into the chapter title **How Encryption Works**, then shrinks to a corner tag that stays on screen for the chapter. |

### 2. Plaintext and ciphertext (0:14–0:48)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:14–0:24 | "At its most basic level, encryption is the process of transforming readable information into an unreadable format so that unauthorized people cannot understand it." | "Meet at 3pm" writes on in green. An arrow grows right; a scrambled red copy appears. A gray observer leans in and a "?" pops above its head. |
| 0:24–0:27 | "The original readable information is called plaintext." | The green text pulses; label **PLAINTEXT**. |
| 0:27–0:33 | "Encryption uses a mathematical algorithm and a key to transform the plaintext into ciphertext." | The arrow becomes a pipeline: PLAINTEXT box → blue **ALGORITHM** box with turning gears → **CIPHERTEXT** box. A gold **KEY** plugs into the algorithm from above. |
| 0:33–0:38 | "Ciphertext may look like a random sequence of letters, numbers, or symbols." | Real AES-256-GCM output types out in red: `43d9d0aa954df79d3bd8c4ab98d9cbed4ffddc6e1aae9365dbb646`. It briefly re-renders as Base64 to show other encodings. |
| 0:38–0:48 | "Although the ciphertext still contains the original information, it is designed to be meaningless to anyone who does not have the correct key." | A gray key tries the algorithm in reverse and produces only noise and a red ✗. Small caption: "same information, unreadable without the key". |

### 3. Decryption (0:48–0:59)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:48–0:56 | "The intended recipient can then use a key and a decryption algorithm to convert the ciphertext back into plaintext." | The pipeline mirrors right to left. Sam on the right plugs in the gold key; red ciphertext flows back through the gears and comes out green. |
| 0:56–0:58 | "This process is called decryption." | Labels settle: **ENCRYPTION** over the forward arrow, **DECRYPTION** over the return arrow, forming a closed loop. |
| 0:58–0:59 | *(transition)* | The whole loop diagram collapses into a small wooden box. |

### 4. Locked-box analogy (0:59–1:25)

| Time | Narration | On screen |
| --- | --- | --- |
| 0:59–1:02 | "A simple analogy is a locked box." | The box sits center screen, lid open. |
| 1:02–1:06 | "The plaintext is the message placed inside the box." | The green note drops in; a dotted line connects it to a **plaintext** label. |
| 1:06–1:09 | "The encryption algorithm is the locking mechanism," | The lid shuts and a padlock snaps on; label **algorithm**. |
| 1:09–1:14 | "and the key is what allows the box to be opened." | The gold key appears beside it; label **key**. |
| 1:14–1:24 | "Anyone might be able to see the locked box, but only someone with the correct key should be able to access the message." | The box travels along network lines past three gray observers who can see it but not open it. Sam turns the gold key; the lid opens and the note glows green. |
| 1:24–1:25 | *(transition)* | Camera zooms into the padlock's keyhole. |

### 5. Mathematics, not hiding (1:25–1:41)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:25–1:30 | "Modern encryption is based on mathematics rather than simply hiding information." | Split screen. Left, **hiding**: a note slipped under a rug, which a gray hand lifts (✗). Right, **math**: bits pass through an equation-like transform (✓). Small caption: "The algorithm can be public; only the key is secret." |
| 1:30–1:36 | "Algorithms are designed so that encrypting information is easy when the correct key is available," | With the gold key, a message passes through the algorithm in one quick flash, marked with a green ✓. |
| 1:36–1:40 | "but reversing the process without the key is computationally impractical." | Without the key, a counter starts guessing keys. Caption: **2¹²⁸ ≈ 3.4 × 10³⁸ possible keys** for a 128-bit key. A progress bar beneath it stays at 0.000…%. |
| 1:40–1:41 | *(transition)* | The counter freezes and drops down into the base of a pillar. |

### 6. What makes encryption strong (1:41–2:22)

| Time | Narration | On screen |
| --- | --- | --- |
| 1:41–1:45 | "The strength of encryption depends on several factors." | Three empty pillar outlines rise from the floor. |
| 1:45–1:48 | "These include the quality of the algorithm," | Pillar 1 fills: **Algorithm quality**. A vetted AES card stands firm while a homemade cipher card cracks. |
| 1:48–1:51 | "the length and randomness of the key," | Pillar 2 fills: **Key length and randomness**. A bar grows through 56 → 128 → 256 bits; random bits shown beside a weak pattern "password123". |
| 1:51–1:54 | "and how securely the key is stored." | Pillar 3 fills: **Key storage**. A key inside a vault icon vs. a key on a sticky note. |
| 1:54–2:01 | "Even a strong algorithm can be compromised if a key is stolen, guessed, or accidentally exposed." | Three mini icons, one per verb: a hand grabbing a key (stolen), dice rolling (guessed), a key visible on a public screen (exposed). |
| 2:01–2:10 | "For example, if an attacker obtains a password used to protect an encrypted file, the encryption itself may not be broken." | A gray attacker reads a sticky note with a password. The encrypted file's padlock stays intact, with no cracks. |
| 2:10–2:15 | "Instead, the attacker has obtained the key needed to unlock the information." | Arrow: **password → key derivation → key**. The derived gold key opens the file cleanly. |
| 2:15–2:21 | "This is why key management is one of the most important parts of cybersecurity." | A ring diagram draws: **generate → store → distribute → rotate → revoke**, with a key moving around the ring. |
| 2:21–2:22 | *(transition)* | Corner tag changes from 1 to **2 Types of Encryption**. |

**Chapter 2: Types of Encryption (2:22–5:25)**

### 7. Symmetric encryption (2:22–3:11)

| Time | Narration | On screen |
| --- | --- | --- |
| 2:22–2:24 | *(music only)* | Chapter card: **Types of Encryption**. |
| 2:24–2:29 | "There are two major categories of encryption: symmetric encryption and asymmetric encryption." | Two panels appear side by side: **SYMMETRIC** (one gold key) and **ASYMMETRIC** (blue + gold key pair). |
| 2:29–2:34 | "Symmetric encryption uses the same key for both encryption and decryption." | The asymmetric panel dims. One gold key sits under both the lock and unlock arrows. |
| 2:34–2:42 | "The sender uses the key to encrypt the message, and the recipient uses that same key to decrypt it." | Maya locks with her copy of the gold key; Sam unlocks with an identical copy. An "=" sign pulses between the two keys. |
| 2:42–2:49 | "Symmetric encryption is generally fast and efficient, which makes it useful for encrypting large amounts of data." | A large stack of data blocks streams through the algorithm quickly; a disk icon fills with locked blocks. |
| 2:49–2:55 | "Common symmetric encryption algorithms include the Advanced Encryption Standard, or AES, and ChaCha20." | Two spec cards flip in. **AES**: block cipher, 128-bit blocks, 128/192/256-bit keys. **ChaCha20**: stream cipher, 256-bit key, fast in software. |
| 2:55–3:02 | "However, symmetric encryption creates an important challenge: both parties need to obtain the same secret key securely." | The cards slide away. A copy of the gold key must travel from Maya to Sam along a dashed channel. |
| 3:02–3:10 | "If the key is sent through an insecure channel and intercepted, an attacker may be able to decrypt the communication." | A gray attacker (Eve) copies the key mid-channel, then uses it to decrypt Maya's stream; the stream turns green on Eve's side. Red alert outline. |
| 3:10–3:11 | *(transition)* | Eve's copied key cracks and splits into two keys: blue and gold. |

### 8. Asymmetric encryption (3:11–4:16)

| Time | Narration | On screen |
| --- | --- | --- |
| 3:11–3:19 | "Asymmetric encryption, also called public-key encryption, uses a pair of mathematically related keys: a public key and a private key." | The asymmetric panel brightens. A blue **PUBLIC KEY** and a gold **PRIVATE KEY** sit side by side, joined by a thin glowing line labeled "mathematically related". |
| 3:19–3:22 | "The public key can be shared openly." | Copies of the blue key fan out to five figures around the screen. |
| 3:22–3:25 | "The private key must be kept secret." | The gold key moves into a small vault next to Sam. |
| 3:25–3:32 | "Information encrypted with the public key can generally be decrypted only with the corresponding private key." | A message locks with the blue key. A blue key tries to unlock it (✗); the gold key unlocks it (✓). |
| 3:32–3:42 | "For example, if someone wants to send a secure message to a recipient, they can encrypt the message using the recipient’s public key." | Maya picks up Sam's blue key from a public directory and locks her message with it. |
| 3:42–3:47 | "Only the recipient’s private key should be able to decrypt it." | Eve also holds a copy of the blue key but can't open the message. Sam opens it with his gold key. |
| 3:47–3:55 | "Asymmetric encryption solves much of the key-distribution problem because the public key does not need to be kept secret." | Callback to Scene 7: the dashed channel returns. Eve intercepts the blue key this time and gets nothing useful; a shrug icon appears. |
| 3:55–4:00 | "However, it is typically slower and more computationally expensive than symmetric encryption." | Two horizontal throughput bars race: symmetric fills quickly, asymmetric crawls. Qualitative only, with no numbers. |
| 4:00–4:05 | "Examples of public-key algorithms include RSA and elliptic-curve cryptography, often called ECC." | Two cards. **RSA**: two large primes multiply into a huge number (factoring is hard). **ECC**: Manim draws the curve y² = x³ + ax + b and points hop along it. |
| 4:05–4:15 | "ECC can provide strong security with shorter key sizes, which makes it useful in mobile devices, web browsers, and other systems with limited resources." | Bar chart at roughly equal security (128-bit level): **RSA 3072-bit** long bar vs. **ECC 256-bit** short bar. Then three icons pop in: phone, browser, small chip. |
| 4:15–4:16 | *(transition)* | Both panels slide together and merge into one. |

### 9. Hybrid encryption and HTTPS (4:16–4:47)

| Time | Narration | On screen |
| --- | --- | --- |
| 4:16–4:22 | "In practice, many modern systems use a hybrid approach that combines both types." | The merged panel shows the blue/gold key pair on top feeding into a gold session key below. |
| 4:22–4:26 | "For example, when a user visits a website using HTTPS," | A laptop with a browser bar (padlock + "https://") on the left, a server on the right. |
| 4:26–4:34 | "asymmetric cryptography can help the browser and the server authenticate each other and establish a shared session key." | The server sends a certificate card; the browser checks its signature (✓). Then both sides each contribute a half; the halves combine into the **same gold session key** on both sides. |
| 4:34–4:42 | "After that, symmetric encryption is usually used to protect the actual data exchanged during the session because it is faster." | A fast stream of small locked data records flows both ways, each marked with the gold session key. |
| 4:42–4:46 | "This combination provides both secure key exchange and efficient communication." | Two check labels appear: **secure key exchange ✓**, **efficient communication ✓**. |
| 4:46–4:47 | *(transition)* | The data stream freezes into a single message card in the center. |

### 10. Hashing and digital signatures (4:47–5:25)

| Time | Narration | On screen |
| --- | --- | --- |
| 4:47–4:51 | "It is also important to distinguish encryption from hashing." | Split screen. **Encryption**: a two-way arrow (encrypt ⇄ decrypt). **Hashing**: a one-way arrow. |
| 4:51–4:59 | "Hashing transforms data into a fixed-length value, called a hash, but it is not designed to be reversed." | "hi" and a full paragraph each pass through **SHA-256**; both outputs are exactly 64 hex characters. An arrow back from hash to input is crossed out. |
| 4:59–5:03 | "Hashing is commonly used to store passwords securely" | A password plus a random **salt** hashes into a row in a database table. At login, the new hash is compared to the stored one (✓). |
| 5:03–5:07 | "and to verify whether data has been changed." | "Meet at 3pm" → `96af04f24c4542d0…`; "Meet at 4pm" → `5bf79f4cb8cd61d5…`. One changed character makes the hash completely different; the differences highlight in red. |
| 5:07–5:13 | "Digital signatures are related to public-key cryptography as well, but they serve a different purpose." | The blue/gold key pair returns, this time owned by Maya. |
| 5:13–5:16 | "Encryption is mainly used to protect confidentiality," | A padlock icon with the label **CONFIDENTIALITY**. |
| 5:16–5:24 | "while digital signatures help verify the identity of the sender and confirm that the message has not been modified." | Maya hashes her message and signs it with her gold private key. Sam verifies with Maya's blue public key (✓). A tampered copy fails verification (✗). |
| 5:24–5:25 | *(transition)* | Corner tag changes to **3 Applications**. |

**Chapter 3: Applications of Encryption (5:25–8:00)**

### 11. Web, messaging and storage (5:25–6:29)

| Time | Narration | On screen |
| --- | --- | --- |
| 5:25–5:27 | *(music only)* | Chapter card: **Applications of Encryption**. |
| 5:27–5:30 | "Encryption is used throughout everyday computing." | A constellation of device icons fades in around a central padlock. |
| 5:30–5:38 | "One of the most familiar examples is HTTPS, which protects communication between a web browser and a website." | Zoom to the browser bar from Scene 9: padlock + "https://". |
| 5:38–5:48 | "When a website uses HTTPS, information such as login credentials, personal details, and payment information is encrypted while traveling across the internet." | Three packets (login, ID card, credit card), one per item, lock and hop across network nodes. Observers at each node see only red. |
| 5:48–5:51 | "Encryption is also used in messaging applications." | Two phones, left and right, with a provider server in the middle. |
| 5:51–6:00 | "End-to-end encryption is designed so that a message is encrypted on the sender’s device and decrypted only on the recipient’s device." | The message locks on phone A and stays locked through the server; it unlocks only on phone B. Label **END-TO-END**. |
| 6:00–6:07 | "Ideally, even the messaging provider cannot read the contents of the message while it is in transit." | A figure at the server looks at the red blob passing through; a "?" appears. |
| 6:07–6:10 | "Another major application is data storage." | The phones fade; a storage shelf appears. |
| 6:10–6:15 | "Computers, smartphones, USB drives, and cloud services can encrypt stored files." | Four icons, one per item (laptop, phone, USB drive, cloud), each get a padlock. |
| 6:15–6:18 | "This is called encryption at rest." | Label **AT REST** appears under the stored files; a small inset of the moving packets from earlier is labeled **IN TRANSIT** for contrast. |
| 6:18–6:28 | "If a device is lost or stolen, encryption can make it much more difficult for someone to access the information stored on it." | A gray hand takes the laptop and opens its drive, which shows only red ciphertext. |
| 6:28–6:29 | *(transition)* | Icons slide aside; a bank building rises. |

### 12. Banking, VPNs and organizations (6:29–7:10)

| Time | Narration | On screen |
| --- | --- | --- |
| 6:29–6:33 | "Encryption is also important in online banking and electronic payments." | A bank building and a card terminal connected by a line. |
| 6:33–6:41 | "Financial institutions use cryptographic protocols to protect account information, verify transactions, and reduce the risk of unauthorized access." | Three beats, one per phrase: account record locks; a transaction gets a signature ✓; an intruder bounces off a shield. |
| 6:41–6:49 | "Virtual private networks, or VPNs, use encryption to protect data traveling between a device and a VPN server." | A laptop in a café on public Wi-Fi. An encrypted tunnel draws from the laptop to a **VPN server**. |
| 6:49–6:55 | "This can help prevent people on the same network from easily viewing the user’s traffic." | A snooper on the café network sees only the tunnel. Past the VPN server, traffic continues on as normal, showing where the protection ends. |
| 6:55–7:02 | "Businesses and governments use encryption to protect confidential records, intellectual property, medical data, and classified information." | Four folders, one per item, each stamped with a padlock. |
| 7:02–7:09 | "In these environments, encryption is often combined with access controls, authentication, monitoring, and other security measures." | Concentric rings draw around the folders, one per item: **encryption**, **access control**, **authentication**, **monitoring**. |
| 7:09–7:10 | *(transition)* | Camera pulls back; small gaps glow between the rings. |

### 13. Limits and conclusion (7:10–8:00)

| Time | Narration | On screen |
| --- | --- | --- |
| 7:10–7:14 | "However, encryption does not solve every security problem." | Spotlights fall on the gaps between the rings. |
| 7:14–7:19 | "It cannot protect data from a person who already has authorized access," | An insider figure with a valid gold key opens a folder normally. |
| 7:19–7:25 | "and it cannot prevent every type of malware, phishing attack, or social-engineering attack." | Three icons, one per item: a bug, a fishhook on an email, a phone-call figure. |
| 7:25–7:31 | "Encryption protects information, but the surrounding systems and users must also be secure." | The locked box sits in the center, surrounded by a computer icon and a person icon, both outlined. |
| 7:31–7:36 | "Overall, encryption supports three major security goals: confidentiality, integrity, and authentication." | Three pillars rise: **CONFIDENTIALITY**, **INTEGRITY**, **AUTHENTICATION**. |
| 7:36–7:45 | "It helps keep information private, helps detect unauthorized changes, and can help verify the identity of the people or systems involved." | Each pillar lights up with its icon from earlier: padlock (Scene 2), changed hash (Scene 10), signature ✓ (Scene 10). |
| 7:45–7:54 | "As more communication, commerce, and personal activity move online, encryption has become a fundamental part of modern computer science and cybersecurity." | Every icon from the video zooms out into a network of glowing nodes forming a globe. |
| 7:54–8:00 | *(music only)* | Title: **Encryption**. End card with group names, course, sources, and "Animated with Manim Community Edition". |

## Manim build guide

Build on the simplified video's shared objects (key, box, padlock, people, phones, mailbox), then add the technical pieces below. Write one Manim `Scene` class per scene; Claude Code can draft each scene from the beat tables above. The starter code in step 5 was test-rendered with Manim Community Edition 0.22.

**1. Setup**

1. Install Manim Community Edition by following the official installation guide. On Linux you also need the Pango development libraries, since Manim's text rendering depends on them.
2. Use only `Text` (not `MathTex` or `Tex`) so you can skip installing LaTeX. Write exponents with Unicode superscripts (2¹²⁸) and use `font="Monospace"` for hex and hashes.
3. Render low quality while iterating and high quality at the end:
   - `manim -pql scenes.py Scene02Pipeline` for a fast 480p preview
   - `manim -qh scenes.py Scene02Pipeline` for the 1080p final

**2. Project structure.** One shared folder for both videos keeps the look identical.

```
encryption-videos/
  common/
    style.py        # colors, fonts, background (same as simplified video)
    assets.py       # shared objects from the simplified plan
    tech_assets.py  # new technical objects (table below)
    values.py       # real AES and SHA-256 strings used on screen
  simplified/
    scenes.py
  professional/
    scenes.py       # Scene00Intro (later) ... Scene13Conclusion
    audio/          # narration per scene + music
    renders/
  edit/             # editor projects that join scenes, audio, captions
```

**3. New technical objects (`tech_assets.py`)**

| Object | Built from | Used in scenes |
| --- | --- | --- |
| `ChapterTag(n, title)` | Small `RoundedRectangle` + `Text`, pinned top-left | 1–13 |
| `HistoryTimeline()` | `NumberLine` with labeled ticks (Caesar, Enigma, DES, AES) | Intro, 1 |
| `Pipeline()` | Input box → `Algorithm` box with `Gear`s → output box, plus a key slot | 2, 3, 5 |
| `HexText(s)` | Monospace `Text`, wrapped into lines, typed with `AddTextLetterByLetter` | 2, 10, 11 |
| `KeyspaceCounter()` | `DecimalNumber` updater + `ProgressBar` that barely moves | 5 |
| `Pillar(label)` | Tall `Rectangle` that fills from the bottom | 6, 13 |
| `LifecycleRing(steps)` | Five labels placed on a `Circle`, with a key moving via `MoveAlongPath` | 6 |
| `SpecCard(title, lines)` | `RoundedRectangle` + title + bullet `Text` lines | 7, 8 |
| `Eve()` | Gray `Person` with a hood (reuse the simplified video's `HoodedFigure`) | 7, 8 |
| `ThroughputBar(label, rate)` | `Rectangle` whose width grows with a `ValueTracker` | 8 |
| `EllipticCurve(a, b)` | `Axes` + `axes.plot_implicit_curve(lambda x, y: y**2 - x**3 - a*x - b)` | 8 |
| `KeySizeBars()` | Two labeled bars: RSA 3072-bit vs. ECC 256-bit | 8 |
| `Certificate()` | Card with a seal `Circle` and a check mark | 9 |
| `SessionKeyMerge()` | Two half-keys that slide together into one gold key, mirrored on both sides | 9 |
| `HashBox()` | `Algorithm` box labeled SHA-256 with a one-way arrow | 10 |
| `DbTable(rows)` | `Table` mobject with user / salt / hash columns | 10 |
| `SignatureFlow()` | Message → hash → sign (gold) → verify (blue) → ✓ or ✗ | 10, 12 |
| `Tunnel(a, b)` | Two parallel curved lines with a moving dash pattern | 12 |
| `DefenseRings(labels)` | Concentric `Circle`s with labels on each ring | 12, 13 |
| `NetworkGlobe()` | `Dot`s on a `Circle` grid joined by `Line`s, rotating slowly | 13 |

**4. Animation recipes per scene**

| # | Core Manim moves |
| --- | --- |
| 1 | `HistoryTimeline` scales to a thin line with `animate.stretch` and shifts off-screen; chapter cards `FadeIn(shift=UP)` timed one per phrase; card 1 becomes the `ChapterTag` with `Transform`. |
| 2 | `Write` plaintext; `GrowArrow`; build `Pipeline` with `Create`; key drops in with `animate.shift(DOWN)`; real ciphertext typed with `AddTextLetterByLetter`; Base64 swap with `Transform`; wrong key produces `ScrambleText` noise. |
| 3 | Mirror the pipeline with `animate.flip()` or rebuild it reversed; flow text right to left; labels `Write` above and below to make the loop. |
| 4 | `Transform` the pipeline into the `Box`; label lines with `Create(DashedLine(...))`; box travels with `MoveAlongPath` past observers; lid opens with `Rotate`. |
| 5 | `MovingCameraScene` zoom into the keyhole; split screen with two `VGroup`s; `KeyspaceCounter` uses an updater on a `DecimalNumber`. |
| 6 | Pillars fill with `animate.stretch_to_fit_height` from the bottom edge; key-length bar grows through 56 → 128 → 256 with `Transform` on its label; `LifecycleRing` with `MoveAlongPath`. |
| 7 | Panels as `RoundedRectangle`s; `TransformFromCopy` for the duplicate key; data blocks stream with `LaggedStart`; spec cards flip with `Rotate(axis=UP)`; Eve copies the key with `TransformFromCopy` mid-path. |
| 8 | `ReplacementTransform` one key into two; blue key copies fan out with `LaggedStart`; `ThroughputBar`s race with `ValueTracker`s at different rates; `EllipticCurve` drawn with `Create`, points hop with `MoveAlongPath`; `KeySizeBars` grow with `GrowFromEdge(LEFT)`. |
| 9 | `Certificate` slides across, then `Indicate` the check mark; `SessionKeyMerge` on both sides simultaneously; records stream with `LaggedStart` in both directions. |
| 10 | Split screen arrows; inputs flow into the `HashBox` and outputs type out as `HexText`; reverse arrow crossed with a red `Cross`; avalanche highlight (starter code); `SignatureFlow` step by step. |
| 11 | Packets hop node to node with `Succession(MoveAlongPath...)`; E2EE lock/unlock only at the ends; padlocks stamp with `animate.scale(1.3)` then back; laptop taken by a `GrabHand`. |
| 12 | `Tunnel` drawn with `Create` and a dash updater; snooper icon `Wiggle`s; folders stamped; `DefenseRings` draw outward with `LaggedStart(Create(...))`. |
| 13 | Spotlight with a semi-transparent `Annulus` or an `Indicate` on each gap; pillars rise; earlier icons `TransformFromCopy` onto each pillar; everything shrinks into `NetworkGlobe`. |

**5. Starter code (test-rendered).** `values.py` generates the real values shown on screen; the two scenes below cover the pipeline beat in Scene 2 and the avalanche beat in Scene 10.

```python
# common/values.py: real values for the screen (demo key only, never reuse)
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key, nonce = bytes(range(32)), bytes(12)
AES_HEX = AESGCM(key).encrypt(nonce, b"Meet at 3pm", None).hex()
# -> 43d9d0aa954df79d3bd8c4ab98d9cbed4ffddc6e1aae9365dbb646
SHA_3PM = hashlib.sha256(b"Meet at 3pm").hexdigest()
SHA_4PM = hashlib.sha256(b"Meet at 4pm").hexdigest()
```

```python
from manim import *
import hashlib

BG, PLAIN, CIPHER, KEYC, ALGO, LABEL = (
    "#14213D", "#3DDC97", "#FF6B4A", "#FFC93C", "#3A86FF", "#F1FAEE")
config.background_color = BG

# Real AES-256-GCM output for "Meet at 3pm" (demo key 00..1f, zero nonce)
AES_HEX = "43d9d0aa954df79d3bd8c4ab98d9cbed4ffddc6e1aae9365dbb646"


def key_icon(color=KEYC):
    bow = Circle(radius=0.22, color=color, stroke_width=6)
    shaft = Line(bow.get_right(), bow.get_right() + RIGHT * 0.7,
                 color=color, stroke_width=6)
    t1 = Line(shaft.get_end(), shaft.get_end() + DOWN * 0.2, color=color, stroke_width=6)
    t2 = t1.copy().shift(LEFT * 0.2)
    return VGroup(bow, shaft, t1, t2)


class Scene02Pipeline(Scene):
    """Beat 0:27-0:38: plaintext -> ALGORITHM (+key) -> real ciphertext."""
    def construct(self):
        plain = Text("Meet at 3pm", color=PLAIN, font_size=34).to_edge(LEFT, buff=0.5)
        plain_lbl = Text("PLAINTEXT", color=PLAIN, font_size=20).next_to(plain, DOWN)

        algo = RoundedRectangle(width=2.6, height=1.4, corner_radius=0.2,
                                color=ALGO, fill_opacity=0.15)
        algo_lbl = Text("ALGORITHM", color=ALGO, font_size=22).move_to(algo)
        key = key_icon().next_to(algo, UP, buff=0.6)
        key_lbl = Text("KEY", color=KEYC, font_size=20).next_to(key, RIGHT)

        a1 = Arrow(plain.get_right(), algo.get_left(), buff=0.2, color=LABEL)
        out_pos = algo.get_right() + RIGHT * 1.1
        cipher = Text(AES_HEX[:18] + "\n" + AES_HEX[18:36] + "\n" + AES_HEX[36:],
                      font="Monospace", color=CIPHER, font_size=20,
                      line_spacing=0.8).next_to(out_pos, RIGHT, buff=0.3)
        a2 = Arrow(algo.get_right(), cipher.get_left(), buff=0.2, color=LABEL)
        cipher_lbl = Text("CIPHERTEXT", color=CIPHER, font_size=20).next_to(cipher, DOWN)

        self.play(Write(plain), FadeIn(plain_lbl))
        self.play(GrowArrow(a1), Create(algo), Write(algo_lbl))
        self.play(FadeIn(key, shift=DOWN * 0.3), FadeIn(key_lbl))
        self.play(VGroup(key, key_lbl).animate.shift(DOWN * 0.55), run_time=0.6)
        self.play(GrowArrow(a2), AddTextLetterByLetter(cipher, time_per_char=0.03))
        self.play(FadeIn(cipher_lbl))
        self.wait(1)


class Scene10Avalanche(Scene):
    """Beat 5:03-5:07: one changed character -> completely different SHA-256."""
    def construct(self):
        rows = VGroup()
        hashes = []
        for msg in ["Meet at 3pm", "Meet at 4pm"]:
            h = hashlib.sha256(msg.encode()).hexdigest()
            hashes.append(h)
            m = Text(f'"{msg}"', color=PLAIN, font_size=28)
            arrow = Arrow(ORIGIN, RIGHT * 1.2, color=LABEL)
            hx = Text(h[:32] + "\n" + h[32:], font="Monospace",
                      font_size=18, color=LABEL, line_spacing=0.8)
            rows.add(VGroup(m, arrow, hx).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.9)
        title = Text("SHA-256", color=ALGO, font_size=30).to_edge(UP)

        self.play(Write(title))
        for r in rows:
            self.play(Write(r[0]), GrowArrow(r[1]))
            self.play(AddTextLetterByLetter(r[2], time_per_char=0.01))
        # highlight characters that differ (text glyphs skip the newline)
        a, b = hashes
        diff = [i for i in range(64) if a[i] != b[i]]
        self.play(*[rows[1][2][i].animate.set_color(CIPHER) for i in diff])
        self.wait(1)
```

**6. Syncing to the narration.** Treat each beat's time window as its duration. In each scene, sum the `run_time` of the animations in a beat, then add `self.wait()` to fill the rest of the window. Once the narration is recorded, measure each sentence and update the windows. When the intro is finished, shift every timecode by its length; the beat order doesn't change. The `manim-voiceover` plugin is an optional way to time animations to the narration automatically.

## Proof-of-concept test

Build Scenes 2, 8 and 10 first (0:14–0:48, 3:11–4:16 and 4:47–5:25, about 2:17). They hold the most technical visuals in the video: the pipeline with real ciphertext, the key pair with the elliptic curve and key-size bars, and the hash avalanche with the signature flow. If those read clearly, the rest of the video is easier.

- [ ] Set up the shared `encryption-videos/` folder and copy in `style.py` and `assets.py` from the simplified project
- [ ] Render the two starter scenes (`Scene02Pipeline`, `Scene10Avalanche`) at low quality
- [ ] Build `Pipeline`, `HexText`, `SpecCard`, `EllipticCurve`, `KeySizeBars`, `HashBox` and `SignatureFlow` in `tech_assets.py`
- [ ] Animate Scene 2 end to end, including the wrong-key attempt
- [ ] Animate Scene 8, including the callback to Eve and the throughput race
- [ ] Animate Scene 10, including the salted password table and the tampered-signature ✗
- [ ] Record narration for those scenes and re-time each beat window to the real audio
- [ ] Join renders and audio in an editor (DaVinci Resolve, CapCut or Canva) and add captions
- [ ] Review as a group: can a technical viewer follow every step, and does each visual land on its words?

**If it works,** build the remaining scenes in order and slot the intro in front once it's written. **If the video runs long,** trim the transitions and music cards first (about 22 seconds total), then shorten the busiest beats in Scenes 8 and 11 rather than cutting script.
