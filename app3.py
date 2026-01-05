import pickle
import streamlit as st

# SMS Dectection

tf = pickle.load(open('tff.pkl', 'rb'))
model = pickle.load(open('mnb.pkl', 'rb'))



import re
def cleanEmail(txt):
    clean_text = re.sub(r'http\S+\s', ' ', txt)
    clean_text = re.sub(r'RT|cc', ' ', clean_text)
    clean_text = re.sub(r'#\S+\s', ' ', clean_text)
    clean_text = re.sub(r'@\S+', ' ', clean_text)
    clean_text = re.sub(r'[^\w\s]', ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = clean_text.lower()
    return clean_text

def main():
    st.title('SMS Detection')
    uploaded_email = st.file_uploader('Upload your SMS ')
    user_input = st.text_area("Enter your message : ")

    if st.button("Predict"):
        transfrom_sms = tf.transform([user_input])
        prediction = model.predict(transfrom_sms)[0]
        result = "🚨 SPAM" if prediction == 1 else "✅ SAFE (Not-Spam)"
        st.header(result)

    elif uploaded_email:
        try:
            email_byte = uploaded_email.read()
            email_decode = email_byte.decode('utf-8')
        except UnicodeDecodeError:
            email_decode = email_byte.decode('latin-1')

        clean_email = cleanEmail(email_decode)
        clean_email = tf.transform([clean_email])
        prediction_id = model.predict(clean_email)[0]
        upload_result = "🚨 SPAM" if prediction_id == 1 else "✅ SAFE (Not-Spam)"
        st.header(upload_result)
       



main()
