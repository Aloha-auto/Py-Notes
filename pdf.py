import pydf
import requests
import os

URL = os.environ['URL'] #jsonbin
API_KEY = os.environ['API_KEY'] #jsonbin
test_subject = os.environ['test_subject'] #ntfy test

requests.post(f"https://ntfy.sh/{test_subject}", data="Pdf is running")

dic = requests.get(URL, headers={"authorization": f"token {API_KEY}"}).json()

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relevé de notes</title>
    <style>
        body {{
            font-family: Verdana, Geneva, Tahoma, sans-serif;
        }}
        table.semestre {{
            width: 100%;
            background-color: #ffffff;
            border-collapse: collapse;
            border-width: 1px;
            border-color: #ababab;
            border-style: solid;
            color: #000000;
        }}
        
        table.semestre td, table.semestre th {{
            border-width: 1px;
            border-color: #ababab4b;
            border-style: solid;
            padding: 16px;
        }}
        
        table.semestre thead {{
            background-color: #ababab4b;
        }}
    </style>
</head>
<body>
    <table class="semestre">
        <thead>
            <tr>
                <th>UE</th>
                <th>Matiere</th>
                <th>Note</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Humanités</td>
                <td>EPS</td>
                <td>{dic["Humanités"]["EPS2-S1"]["note"] if dic["Humanités"]["EPS2-S1"]["note"] != "Aucun résultat" else "-"}</td>
            </tr>
            <tr>
                <td>Humanités</td>
                <td>CSS</td>
                <td>{dic["Humanités"]["Cultures. Sciences. Sociétés 3"]["note"] if dic["Humanités"]["Cultures. Sciences. Sociétés 3"]["note"] != "Aucun résultat" else "-"}</td>
            </tr>
            <tr>
                <td>Humanités</td>
                <td>Anglais</td>
                <td>{dic["Humanités"]["L-ANG-FC-2-S1"]["note"] if dic["Humanités"]["L-ANG-FC-2-S1"]["note"] != "Aucun résultat" else "-"}</td>
            </tr>
            <tr>
                <td>Mécanique et environnement</td>
                <td>Conception</td>
                <td>{dic["systèmes Mécaniques et Environnement"]["Conception-Prototypage"]["note"] if dic["systèmes Mécaniques et Environnement"]["Conception-Prototypage"]["note"] != "Aucun résultat" else "-"}</td>
            </tr>
            <tr>
                <td>Mécanique et environnement</td>
                <td>ETRE</td>
                <td>{dic["systèmes Mécaniques et Environnement"]["Enjeux de la Transition Ecologique 2 (sauf asinsa)"]["note"] if dic["systèmes Mécaniques et Environnement"]["Enjeux de la Transition Ecologique 2 (sauf asinsa)"]["note"] != "Aucun résultat" else "-"}</td>
            </tr>
            <tr>
                <td>Mécanique et environnement</td>
                <td>Mécanique des systèmes</td>
                <td>{dic["systèmes Mécaniques et Environnement"]["Mécanique des systèmes 1"]["note"] if dic["systèmes Mécaniques et Environnement"]["Mécanique des systèmes 1"]["note"] != "Aucun résultat" else "-"}</td>
            </tr>
            <tr>
                <td>Mathématiques et numérique</td>
                <td>Mathématiques</td>
                <td>{dic["Mathématiques et Numérique"]["Mathématiques 3"]["note"] if dic["Mathématiques et Numérique"]["Mathématiques 3"]["note"] != "Aucun résultat" else "-"}</td>
            </tr>
            <tr>
                <td>Mathématiques et numérique</td>
                <td>Informatique</td>
                <td>{dic["Mathématiques et Numérique"]["Informatique et Société Numérique 3"]["note"] if dic["Mathématiques et Numérique"]["Informatique et Société Numérique 3"]["note"] != "Aucun résultat" else "-"}</td>
            </tr>
            <tr>
                <td>Physique et chimie</td>
                <td>Chimie</td>
                <td>{"-"}</td>
            </tr>
            <tr>
                <td>Physique et chimie</td>
                <td>Electromagnétisme</td>
                <td>{"-"}</td>
            </tr>
        </tbody>
    </table>
</body>
</html>"""


pdf = pydf.generate_pdf(html)


with open('notes.pdf', 'wb') as f:
    f.write(pdf)
