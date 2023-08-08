


# Bu kodumuzda ise API yi oluşturarak uygulamamızın diğer uygulamalarla bağlantı kurmasını sağlıyoruz.
# Yazılım uygulamalarının birbirleriyle konuşmasını sağlayan bir arayüzdür.
# Uygulamalar, API'ları kullanarak veri alabilir, işlevleri çağırabilir veya farklı sistemlerle iletişim kurabilir. 


#In this code, we are creating an API to enable our application to connect with other applications.
#An API is an interface that allows software applications to communicate with each other.
#Applications can use APIs to retrieve data, invoke functions, or communicate with different systems.


from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from employee_management import Calisan, create_table, performans_puanlama, performans_siniflandirma, calisan_ekle, calisan_sil, calisanlari_listele
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

#-----------------------------------------------------------

host = 'localhost'
port = '5432'
database = 'performans'
user = 'postgres'
password = 'admin'

engine = create_engine(f'postgresql://postgres:admin@localhost:5432/performans')
Session = sessionmaker(bind=engine)

#------------------------------------------------------------

create_table()
@app.route('/')
def home():
    return "Welcome to the Employee Management API!"

#------------------------------------------------------------

@app.route('/employee_add', methods=['POST'])
def api_calisan_ekle():
    if request.method == 'POST':
        data = request.json
        isim = data.get('isim')
        is_saati_uyum = int(data.get('is_saati_uyum'))
        task_puani = int(data.get('task_puani'))
        iletisim = int(data.get('iletisim'))
        proje_uyum = int(data.get('proje_uyum'))

        toplam_puan = performans_puanlama(is_saati_uyum, task_puani, iletisim, proje_uyum)
        performans_sinif = performans_siniflandirma(toplam_puan)

        calisan_ekle(isim, is_saati_uyum, task_puani, iletisim, proje_uyum, toplam_puan)

        response = {
            'message': 'Çalışan başarıyla eklendi.',
            'isim': isim,
            'toplam_puan': toplam_puan,
            'performans_sinif': performans_sinif
        }
        return jsonify(response), 200
#-----------------------------------------------------       

@app.route('/employee_delete/<int:calisan_id>', methods=['DELETE'])
def api_calisan_sil(calisan_id):
    if request.method == 'DELETE':
        calisan_sil(calisan_id)
        response = {
            'message': f'Çalışan (ID: {calisan_id}) başarıyla silindi.'
        }
        return jsonify(response), 200
    
#-----------------------------------------------------   

@app.route('/employee_list', methods=['GET'])
def api_calisanlari_goruntuleme():
    try:
        calisanlar = calisanlari_listele()
        response = []
        for calisan in calisanlar:
            response.append({
                'id': calisan.id,
                'isim': calisan.isim,
                'toplam_puan': calisan.toplam_puan
            })
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-----------------------------------------------------   
    
if __name__ == '__main__':
    app.run(debug=True)

# npm start 