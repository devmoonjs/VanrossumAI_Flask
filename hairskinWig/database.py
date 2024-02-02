import os
import pymysql
import binascii
import zipfile
from io import BytesIO

def save_data_to_database(file_path, diagnosis_result, alter_predict, userid):
    try:
        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='qwer1234', db='bald', charset='utf8')
        cursor = db.cursor()
        
        # 이미지 파일을 바이너리 모드로 열기
        with open(file_path, "rb") as image_file:
            # 이미지 데이터를 읽기
            image_binary = image_file.read()

        # 이미지 데이터를 텍스트 파일에 쓰기 위해 바이너리 데이터를 16진수 문자열로 변환
        hex_data = binascii.hexlify(image_binary).decode("utf-8")

        # SQL
        sql = "INSERT INTO Analysis (user_id, image, result1, result2, result3, result4, result5, result6, finalResult, analysis_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"
        cursor.execute(sql, (userid, hex_data, alter_predict[0], alter_predict[1], alter_predict[2], alter_predict[3], alter_predict[4], alter_predict[5], diagnosis_result))
        db.commit()
        
    except Exception as e:
        # 에러 출력
        print("Error:", str(e))
        db.rollback()

    finally:
        # DB 종료
        cursor.close()
        db.close()
        pass

def get_image_data(userid):
    try:
        output_directory = "./get_analysis_data"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='qwer1234', db='bald', charset='utf8')
        cursor = db.cursor()

        # 이미지 데이터와 텍스트 데이터를 가져오기 위한 쿼리
        # 이미지 데이터와 텍스트 데이터를 가져오기 위한 쿼리
        sql = "SELECT image, finalResult, analysis_date FROM Analysis WHERE user_id = %s ORDER BY number ASC"
        cursor.execute(sql, (userid,))
        results = cursor.fetchall()

        zip_file_path = f"{output_directory}/image_data.zip"

        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            data_list = []

            for index, result in enumerate(results):
                image_data, text_data, analysis_date = result
                # 이미지 데이터를 16진수 문자열에서 바이너리로 변환
                hex_data = image_data
                image_binary = binascii.unhexlify(hex_data)

                # 이미지를 BytesIO로 감싸기
                image_io = BytesIO(image_binary)

                # 이미지를 zip 파일에 추가
                image_name = f"image_{index + 1}.jpg"
                zipf.writestr(image_name, image_io.getvalue())

                # 텍스트 데이터와 날짜를 리스트에 추가
                data_list.append({
                    'text_data': text_data,
                    'analysis_date': analysis_date,
                })

                print(f"Image {index + 1} added to the ZIP archive")

            # Save text data to 'analysisinfo.txt' in the ZIP archive
            with zipf.open('analysisinfo.txt', 'w') as info_file:
                info_content = '\n'.join([f"{data['text_data']} - {data['analysis_date']}" for data in data_list])
                info_file.write(info_content.encode('utf-8'))

        db.close()

        print(f"ZIP file saved to {zip_file_path}")
        return zip_file_path

    except Exception as e:
        print("Error:", str(e))
        return None, None

def save_wigSynthesis(id, ref_path, source_path, synthesis_output):
    try:
        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='qwer1234', db='bald', charset='utf8')
        cursor = db.cursor()
        
        # 이미지 파일을 바이너리 모드로 열기
        with open(ref_path, "rb") as image_file:
            # 가발 이미지 읽어오기
            ref_image_binary = image_file.read()

        # 이미지 데이터를 텍스트 파일에 쓰기 위해 바이너리 데이터를 16진수 문자열로 변환
        ref_hex_data = binascii.hexlify(ref_image_binary).decode("utf-8")

        with open(source_path, "rb") as image_file:
            # 합성 결과 읽어오기
            source_image_binary = image_file.read()

        source_hex_data = binascii.hexlify(source_image_binary).decode("utf-8")

        with open(synthesis_output, "rb") as image_file:
            # 합성 결과 읽어오기
            result_image_binary = image_file.read()

        result_hex_data = binascii.hexlify(result_image_binary).decode("utf-8")
        

        # SQL
        sql = "INSERT INTO SynthesisResult (id, selectWig, userFace, synResult) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id, ref_hex_data, source_hex_data, result_hex_data))
        db.commit()
        
    except Exception as e:
        # 에러 출
        print("Error:", str(e))
        db.rollback()

    finally:
        # DB 종료
        cursor.close()
        db.close()
        pass
