import streamlit as st
import pickle

# List for prediction
input_data = []

# List for giving data on next page
Full_data = []


# ----------------------------- Functions for encoding ----------------------#

# For encoding Gender
def gender(Gen):
    if Gen == "Male":
        return 1
    else:
        return 0


# For encoding BMI
def bmi(bmi):
    if bmi == "Normal":
        return 0
    if bmi == "Obese":
        return 1
    else:
        return 2


# For encoding Occupation
def occ_simplification(occupation):
    encoded_list = [0, 0, 0, 0, 0]
    list_occ = ['Doctor', 'Engineer', 'Lawyer', 'Nurse', 'Teacher']

    if occupation in list_occ:
        index = list_occ.index(occupation)
        encoded_list[index] = 1

    return encoded_list


# ------------------------------------ Function for Prediction on the basis of given input -----------------------#
def prediction(input_val, data_val):
    with open(r"D:\data_science\its_myworld\Sleep_disorder\model_file", 'rb') as f:
        model_obj = pickle.load(f)
    disorder = model_obj.predict([input_val])
    st.title("Your Report")
    data(data_val)

    if disorder == 0:
        return st.success('You are perfectly Fine')
    elif disorder == 1:
        return st.error("You are suffering from Insomania, Consult a Doctor now")
    elif disorder == 2:
        return st.error("You are suffering from Sleep Apnea, Consult a Doctor now")


# -------------------------------- Function for giving values on next page -----------------------------------#
def data(l):
    name, age, gen, sd, qs, pa, sl, bmi, hr, ds, occupation, s_bp, d_bp = l
    col1, col2 = st.columns(2)

    with col1:
        st.write("Name:")
        st.write('Gender:')
        st.write("Age:")
        st.write('Sleep Duration:')
        st.write('Quality of Sleep:')
        st.write("Physical Activity Level:")
        st.write("Stress Level:")
        st.write("BMI Category:")
        st.write("Heart Rate:")
        st.write("Daily Steps:")
        st.write("Occupation:")
        st.write("Blood Pressure:")
    with col2:
        st.write(name)
        st.write(str(gen))
        st.write(str(age))
        st.write(str(sd))
        st.write(str(qs))
        st.write(str(pa))
        st.write(str(sl))
        st.write(str(bmi))
        st.write(str(hr))
        st.write(str(ds))
        st.write(str(occupation))
        st.write(str(s_bp), '/', str(d_bp))


# ------------------------------- Functionality of button -------------------------------------------------------#
def submittt():
    st.session_state['sd'] = 'Prediction_Page'
    st.session_state.input_data = input_data
    st.session_state.full_data = Full_data


# ------------------------------- Creation of form ------------------------------------------------------#
def page1():
    st.image(r"D:\data_science\its_myworld\Sleep_disorder\Streamlit\pic1.png", width=450)
    st.subheader("Fill Your Details")

    # Name of a user
    Name = st.text_input("Name", key="name")

    # To take input for gender ('Male' and 'Female')
    Gender = st.selectbox("Gender", ('Select', 'Male', 'Female'))

    # To take input for age
    Age = st.number_input("Age", value=None, placeholder="Enter your Age", min_value=25, max_value=90)

    # To take input for duration of sleep
    # Sleep_duration = st.select_slider('Sleep Duration', options=[i for i in range(5, 10)])
    Sleep_duration = st.number_input('Sleep Duration', placeholder="Enter the duration of Sleep", value=None)

    # To take input for quality of sleep
    quality_ofSleep = st.select_slider('Quality of Sleep', options=[i for i in range(4, 10)])

    # To take input of Physical activity of user
    Physical_activity = st.select_slider('Physical Activity Level', options=[i for i in range(30, 91)])

    # To take input of stress level
    Stress_level = st.select_slider('Stress Level', options=[i for i in range(3, 9)])

    popover = st.popover("BMI Category Guide ")
    popover.dataframe(
        {'BMI category': ['Normal', 'Overweight', 'Obese'],
         'BMI Range (kg/m^2)': ["18.5-24.9", "25-30", "30-40 above"]}
    )

    # To take input of Body mass index
    BMI_category = st.radio('BMI Category', ['Normal', 'Overweight', 'Obese'], horizontal=True, index=None)

    # To take input of heart rate
    heart_rate = st.select_slider('Heart Rate', options=[i for i in range(60, 101)])

    # To take input of daily steps covered
    daily_steps = st.number_input("Daily Steps", value=None, placeholder="Enter your steps", min_value=1000)

    # To take input of Occupation
    Occupation = st.radio('Occupation', ['Doctor', 'Engineer', 'Lawyer', 'Nurse', 'Teacher', 'Others'],
                          horizontal=True,
                          index=None)

    # To take input of BP
    st.write('**Blood Pressure**')
    sys_bp = st.number_input("Systolic BP", value=None, placeholder=" ", max_value=145, min_value=90)

    dias_bp = st.number_input("Diastolic BP", value=None, placeholder=" ", max_value=95, min_value=60)

    # Button to submit the all inputs
    submit_button = st.button("Submit", on_click=submittt)

    # Adding values in input_data list
    input_data.extend(
        [gender(Gender), Age, Sleep_duration, quality_ofSleep, Physical_activity, Stress_level, bmi(BMI_category),
         heart_rate, daily_steps, sys_bp, dias_bp])
    input_data.extend(occ_simplification(Occupation))

    # Adding the values in Full_data list
    Full_data.extend([Name, Age, Gender, Sleep_duration, quality_ofSleep, Physical_activity, Stress_level, BMI_category,
                      heart_rate, daily_steps, Occupation, sys_bp, dias_bp])


print('input', input_data)
print(Full_data)


# --------------------------------- Function to handle the working of pages------------------------------#
def main():
    if 'sd' not in st.session_state:
        st.session_state['sd'] = 'Input_Page'
    page = st.session_state['sd']

    if page == 'Input_Page':
        page1()

    if page == 'Prediction_Page':
        prediction(st.session_state.input_data, st.session_state.full_data)


if __name__ == "__main__":
    main()
