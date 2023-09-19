from utils.get_audio_file import get_audio_file
from utils.get_transcription import get_transcription
from utils.get_quiz_array import get_quiz_array
import streamlit as st

def handle_new_quiz():
    st.session_state.show_inputs = True
    for key in st.session_state.keys():
        del st.session_state[key]

def handle_radio_change(current_index):
    st.session_state.index_number = current_index

def handle_next_question(user_choice, current_index):
    if st.session_state.index_number < len(st.session_state.questions) - 1:
        st.session_state.index_number = current_index + 1
        if st.session_state.showing_answers == False:
            choice_index = 0
            for choice in st.session_state.choices[current_index]:
                if choice == user_choice:
                    break
                else:
                    choice_index = choice_index + 1
            
            choice_index = choice_index + 2

            st.session_state.user_answers.append(choice_index)
            
    
    else:
        if st.session_state.showing_answers == False:
            if st.session_state.index_number == len(st.session_state.questions) - 1:
                choice_index = 0
                for choice in st.session_state.choices[current_index]:
                    if choice == user_choice:
                        break
                    else:
                        choice_index = choice_index + 1
                
                choice_index = choice_index + 2

            st.session_state.user_answers.append(choice_index)
        st.session_state.index_number = 0
        st.session_state.showing_answers = True

def handle_video_input():
    main_container = st.empty()
    main_card = main_container.container()
    url = main_card.text_input(label="**Enter your video URL:**")
    gen_quiz_btn = main_card.button(label="Generate quiz", type="primary", key="gen_quiz_button")
    if gen_quiz_btn == True:
        with st.spinner("Please wait..."):
            get_audio_file(url)
            transcription = get_transcription()
            st.session_state.quiz_array = get_quiz_array(transcription)
            handle_quiz(st.session_state.quiz_array)
            main_container.empty()

def handle_quiz(quiz_array):

    st.session_state.show_inputs = False

    # quiz_array = """[[1, "What carries information from the body to the brain?", "Afferent nerves", "Efferent nerves", "Axons", "Dendrites", 1], 
    # [2, "What part of the nervous system controls voluntary movements?", "Autonomic system", "Somatic system", "Sympathetic system", "Parasympathetic system", 2], 
    # [3, "What part of the peripheral nervous system is responsible for arousal?", "Somatic system", "Autonomic system", "Sympathetic system", "Parasympathetic system", 3], 
    # [4, "Which cells in the nervous system provides support and nutrition?", "Glial cells", "Neurons", "Myelin", "Axons", 1], 
    # [5, "What happens when a neuron reaches threshold of excitation?", "It fires", "It stays at resting potential", "It dies", "It slows down", 1], 
    # [6, "What do the terminal buttons of a neuron do?", "Release neurotransmitters", "Receive neurotransmitters", "Insulate the neuron", "Speed up transmission", 1], 
    # [7, "What is the space between two neurons called?", "Terminal button", "Synaptic gap", "Receptor site", "Dendrite", 2], 
    # [8, "What are the dendrites covered in?", "Glial cells", "Myelin", "Receptor sites", "Neurotransmitters", 3], 
    # [9, "What is the function of myelin in a neuron?", "Increase speed of information", "Release neurotransmitters", "Receive neurotransmitters", "Convert electrical impulse into a chemical signal", 1], 
    # [10, "Which part of a neuron converts electrical impulses into chemical signals?", "Cell body", "Axon", "Terminal buttons", "Dendrites", 3]]"""

    quiz_array = eval(quiz_array)

    if "index_number" not in st.session_state:
        st.session_state.index_number = 0
        st.session_state.question_numbers = [item[0] for item in quiz_array]
        st.session_state.questions = [item[1] for item in quiz_array]
        st.session_state.choices = [[item[2], item[3], item[4], item[5]] for item in quiz_array]
        st.session_state.answer_index = [item[6]+1 for item in quiz_array]
        st.session_state.user_answers = []
        st.session_state.total_correct = 0
        st.session_state.showing_answers = False
        st.session_state.show_new_quiz_button = False

    current_index = st.session_state.index_number
    out_of_sentence = "**Question " + str(current_index + 1) + " out of 10**"
    st.header(out_of_sentence)
    possible_choices = st.session_state.choices[current_index]
    disableable_radio_btn = st.empty()
    
    if st.session_state.showing_answers == True:
        correct_answer = st.session_state.choices[current_index][st.session_state.answer_index[current_index] - 2]
        if st.session_state.user_answers[current_index] == st.session_state.answer_index[current_index]:
            st.success(('Correct! The answer is "' + correct_answer + '"'))
        
        else:
            st.error(('Incorrect. The correct answer was "') + correct_answer + '"')
    
        user_current_choice = disableable_radio_btn.radio(
            label=("**" + st.session_state.questions[current_index] + "**"),
            options=possible_choices,
            key="radio_option",
            on_change=handle_radio_change,
            args=(current_index,),
            disabled=True,
            index=st.session_state.user_answers[current_index]-2
        )
    

    if st.session_state.showing_answers == False:
        user_current_choice = disableable_radio_btn.radio(
            label=("**" + st.session_state.questions[current_index] + "**"),
            options=possible_choices,
            key="radio_option",
            on_change=handle_radio_change,
            args=(current_index,)
        )

    next_btn = st.empty()
    
    if current_index == len(st.session_state.questions)-1 and st.session_state.showing_answers == True:
        next_btn.button(label="Start new quiz", on_click=handle_new_quiz, type="primary")
    elif current_index == len(st.session_state.questions)-1:
        next_btn.button(label="Submit", on_click=handle_next_question, args=(user_current_choice, current_index), type="primary")
    else:
        next_btn.button(label="Next question", on_click=handle_next_question, args=(user_current_choice, current_index), type="primary", key="next_question_btn")

def main():
    st.header("**Lumina 🧠🎓**")
    st.markdown('Turn educational video lectures into engaging MCQ based quizzes and automatic assessment. Learning has never been this fun!')

    st.divider()

    if "show_inputs" not in st.session_state:
        st.session_state.show_inputs = True

    if st.session_state.show_inputs == True:
        handle_video_input()
    else:
        handle_quiz(st.session_state.quiz_array)


if __name__ == '__main__':
    main()