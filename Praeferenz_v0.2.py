import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import streamlit as st

if "lang" not in st.session_state:
    st.session_state.lang = "de"

col1, col2, col3 = st.columns([0.8,0.1,0.1])

with col2:
    if st.button("🇬🇧"):
        st.session_state.lang = "en"
        st.rerun()

with col3:
    if st.button("🇩🇪"):
        st.session_state.lang = "de"
        st.rerun()

translations = {
    "de": {
        "title": "Präferenzdemokratisches Abstimmungswerkzeug",
        "enter_question": "Gib die Fragestellung der Umfrage ein:",
        "enter_answers": "Gib die Antwortmöglichkeiten an:",
        "answer_option": "Antwortmöglichkeit",
        "confirm_answers": "Antwortmöglichkeiten bestätigen",
        "enter_scale": "Wenn gewünscht gebt nun die mögliche Skala ein:",
        "minimal_value": "Minimaler Wert: ",
        "maximal_value": "Maximaler Wert: ",
        "min_value_error": "Minimaler Wert muss kleiner als maximaler Wert sein. Bitte erneut eingeben.",
        "anonym": "Wollt ihr anonym abstimmen? (Es werden keine Namen der Teilnehmer*innen angezeigt, sondern nur die Anzahl der Stimmen)",
        "enter_name": "Gib deinen Namen ein:",
        "enter_preference": "Gib deine Zustimmung zu den Antwortmöglichkeiten ein",
        "enter_preference_many": "Gib deine Zustimmung zur Antwortmöglichkeit {answer} ein:",
        "confirm_input": "Eingabe bestätigen",
        "end_vote": "Abstimmung beenden",
        "already_voted": "##### Abgestimmt von:",
        "select_visualization": "Welche Darstellungsoptionen der Ergebnisse sollen angezeigt werden?",
        "scale": "Waage",
        "multiple_bar_plots": "Horizontale Balkendiagramme",
        "text_answer": "Textantwort",
        "show_result": "Zeig das Ergebnis",
        "show_guide_lines": "Zeige Hilfslinien",
        "show_guide_lines_average_point": "Zeige Hilfslinien für Durchschnittspunkt",
        "public_opinion": "Meinung des Volkes",
        "participants": "Teilnehmer",
        "winner_option": "Herzlichen Glückwunsch! Ihr seid zu einem Ergebnis gekommen: Option \"{winner}\" hat gewonnen!",
        "strong_opinion_1": "Die stärkste Meinung hatte {name}.",
        "strong_opinion_2": "Die stärkste Meinung hatten {name1} und {name2}.",
        "strong_opinion_more": "Die stärksten Meinungen hatten {names}.",
        "weak_opinion_1": "Die schwächste Meinung hatte {name}.",
        "weak_opinion_2": "Die schwächste Meinung hatten {name1} und {name2}.",
        "weak_opinion_more": "Die schwächsten Meinungen hatten {names}.",
        "and": "und",
        "draw": "Unentschieden!",
        "draw_2": "Es gibt ein Unentschieden zwischen {winner1} und {winner2}!",
        "draw_more": "Es gibt ein Unentschieden zwischen {winners}!",
        "repeat_vote": "Wollt ihr die Abstimmung nocheinmal wiederholen?",
        "yes_with_same": "Ja, mit denselben Antwortmöglichkeiten",
        "yes_with_new": "Ja, aber mit neuen Antwortmöglichkeiten",
        # "no": "Nö passt",
        "finish": "Abstimmung beenden",
        "vote_finished": "Die Abstimmung ist beendet!",
        "back_to_start": "Eine neue Abstimmung starten?"
    },
    "en": {
        "title": "Preference Democratic Voting Tool",
        "enter_question": "Enter the question of the survey:",
        "enter_answers": "Enter answers:",
        "answer_option": "Option",
        "confirm_answers": "Confirm answers",
        "enter_scale": "If desired, enter the possible range:",
        "minimal_value": "Minimal Value: ",
        "maximal_value": "Maximal Value: ",
        "min_value_error": "Minimal Value must be less than Maximal Value. Please enter again.",
        "anonym": "Do you want to vote anonymously? (No names of participants will be displayed, only the number of votes)",
        "enter_name": "Enter your name:",
        "enter_preference": "Enter your preference for the answer options",
        "enter_preference_many": "Enter your preference for the answer option {answer}:",
        "confirm_input": "Confirm Input",
        "end_vote": "Finish voting",
        "already_voted": "##### Voted by:",
        "select_visualization": "Which visualization options for the results should be displayed?",
        "scale": "Scale",
        "multiple_bar_plots": "Horizontal Bar Charts",
        "text_answer": "Text Answer",
        "show_result": "Show results",
        "show_guide_lines": "Show guide lines",
        "show_guide_lines_average_point": "Show guide lines for average point",
        "public_opinion": "Public vote",
        "participants": "Participants",
        "winner_option": "Congratulations! You have reached a result: Option \"{winner}\" won!",
        "strong_opinion_1": "{name} had the strongest opinion.",
        "strong_opinion_2": "{name1} and {name2} had the strongest opinions.",
        "strong_opinion_more": "{names} had the strongest opinions.",
        "weak_opinion_1": "{name} had the weakest opinion.",
        "weak_opinion_2": "{name1} and {name2} had the weakest opinions.",
        "weak_opinion_more": "{names} had the weakest opinions.",
        "and": "and",
        "draw": "It's a tie!",
        "draw_2": "There is a tie between {winner1} and {winner2}!",
        "draw_more": "There is a tie between {winners}!",
        "repeat_vote": "Do you want to repeat the vote?",
        "yes_with_same": "Yes, with the same options",
        "yes_with_new": "Yes, but with new options",
        # "no": "No, it's fine",
        "finish": "Finish",
        "vote_finished": "The vote is finished!",
        "back_to_start": "Start a new vote?"
    }
}

def t(key, **kwargs):
    text = translations[st.session_state.lang][key]
    return text.format(**kwargs)

if "app_state" not in st.session_state:
    st.session_state.app_state = "voting"   # voting, finished

if "confirmed" not in st.session_state:
    st.session_state.confirmed = False

# st.title("Praeferenzdemokratisches Abstimmungswerkzeug")
st.title(t("title"))


def input_answers():
    # Initialize session state
    if "answers" not in st.session_state:
        st.session_state.answers = ["", ""]

    st.write(t("enter_answers"))

    # Display inputs
    for i in range(len(st.session_state.answers)):
        st.session_state.answers[i] = st.text_input(
            f"{i+1}. {t('answer_option')}:",
            value=st.session_state.answers[i],
            key=f"answer_{i}",
            disabled=st.session_state.confirmed  # Makes fields immutable
        )
    # Add new field automatically if last one is filled
    if not st.session_state.confirmed and st.session_state.answers[0] != "" and st.session_state.answers[1] != "":
        if st.session_state.answers[-1] != "":
            st.session_state.answers.append("")
            st.rerun()
    # st.write(st.session_state.answers)
    # Confirm button
    if not st.session_state.confirmed and st.session_state.answers[0] != "" and st.session_state.answers[1] != "" and st.session_state.answers[-1] == "":
        
        if st.button(t("confirm_answers")):
            
            # Remove last empty field
            if st.session_state.answers[-1] == "":
                st.session_state.answers.pop()

            st.session_state.confirmed = True
            st.rerun()

    # Return confirmed answers
    if st.session_state.confirmed:
        return st.session_state.answers

# answers = input_answers()
# n_answers = len(answers)

def input_min_max(n_answers):

    if "min" not in st.session_state:
        st.session_state.min = 0

    if "max" not in st.session_state:
        st.session_state.max = 5

    if "confirmed_min_max" not in st.session_state:
        st.session_state.confirmed_min_max = False

    st.write(t("enter_scale"))
    if n_answers == 2:
        mini = st.number_input(t("minimal_value"), value=-5, step=1, disabled=st.session_state.confirmed_min_max)
    else:
        mini = st.number_input(t("minimal_value"), value=0, step=1, disabled=st.session_state.confirmed_min_max)
    
    maxi = st.number_input(t("maximal_value"), value=5, step=1, disabled=st.session_state.confirmed_min_max)
    if mini >= maxi:
        st.write(t("min_value_error"))
        st.rerun()
    if not st.session_state.confirmed_min_max:
        if st.button(t("confirm_answers")):
            st.session_state.confirmed_min_max = True
            st.session_state.min = mini
            st.session_state.max = maxi
            st.rerun()
    # Return confirmed answers
    if st.session_state.confirmed_min_max:
        return st.session_state.min, st.session_state.max

# mini, maxi = input_min_max(2)

def input_vote_2(answers, question, mini, maxi):
    
    st.write(question)

    if "votes" not in st.session_state:
        st.session_state.votes = []

    if "finished" not in st.session_state:
        st.session_state.finished = False

    if not st.session_state.finished:

        st.text_input(t("enter_name"), key="name_input")
        st.slider(
            t("enter_preference") + f" ({answers[0]} ↔ {answers[1]}):",
            mini, maxi, 0, key="answer_input"
        )
        
        col1, col2 = st.columns(2)
        def submit_vote():
            name = st.session_state.name_input
            answer = st.session_state.answer_input

            if name != "":
                st.session_state.votes.append({
                    "Name": name,
                    "Answer": answer
                })

                # Reset safely BEFORE next rerun
                st.session_state.name_input = ""
                st.session_state.answer_input = 0
        with col1:
            st.button(t("confirm_input"), on_click=submit_vote, disabled=st.session_state.name_input.strip() == "" )

        with col2:
            st.button(t("end_vote"), on_click=lambda: st.session_state.update({"finished": True}), disabled=len(st.session_state.votes) < 2)
            # st.rerun()
    # show confirmed voters
    if len(st.session_state.votes) > 0:
        st.write(t("already_voted"))
        for vote in st.session_state.votes:
            st.write(f"- {vote['Name']}")
    # st.session_state.votes
    return pd.DataFrame(st.session_state.votes)


def input_vote_many(answers, question, mini, maxi):

    st.write(question)

    if "votes" not in st.session_state:
        st.session_state.votes = []

    if "finished" not in st.session_state:
        st.session_state.finished = False

    # initialize widget state safely
    if "name_input" not in st.session_state:
        st.session_state.name_input = ""

    for i in range(len(answers)):
        key = f"answer_input_{i}"
        if key not in st.session_state:
            st.session_state[key] = 0

    def submit_vote():
        name = st.session_state.name_input
        collected_answers = [
            st.session_state[f"answer_input_{i}"] for i in range(len(answers))
        ]

        if name != "":
            vote_dict = {
                "Name": name,
                **{
                    answers[i]: st.session_state[f"answer_input_{i}"]
                    for i in range(len(answers))
                }
            }

            st.session_state.votes.append(vote_dict)

            # Reset safely BEFORE next rerun
            st.session_state.name_input = ""
            for i in range(len(answers)):
                st.session_state[f"answer_input_{i}"] = 0

    if not st.session_state.finished:
        st.text_input(t("enter_name"), key="name_input")
        for i in range(len(answers)):
            st.slider(
                t("enter_preference_many", answer=answers[i]),
                mini, maxi, value = 0, key=f"answer_input_{i}"
            )
            # st.session_state.answers[i] = answer
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.button(t("confirm_input"), on_click=submit_vote, disabled=st.session_state.name_input.strip() == "" )

        with col2:
            st.button(t("end_vote"), on_click=lambda: st.session_state.update({"finished": True}), disabled=len(st.session_state.votes) < 2)
            # st.rerun()
    # show confirmed voters
    if len(st.session_state.votes) > 0:
        st.write(t("already_voted"))
        for vote in st.session_state.votes:
            st.write(f"- {vote['Name']}")
    # st.session_state.votes
    return pd.DataFrame(st.session_state.votes)

# input_vote_2(["adf", "bcg"], "Wie sehr bist du für bzw. gegen die Antwortmöglichkeiten?", -5, 5)
# input_vote_many(["adf", "bcg", "def"], "Wie sehr bist du für bzw. gegen die Antwortmöglichkeiten?", 0, 5)


def input_visualisation(n_answers):
    st.write(t("select_visualization"))
    chosen_options = []
    if n_answers == 2:
        st.checkbox("Bar Plot", value=True, key="bar_plot")
        if st.session_state.bar_plot:
            chosen_options.append("Bar Plot")
        st.checkbox(t("scale"), value=True, key="scale")
        if st.session_state.scale:
            chosen_options.append("Waage")
        st.checkbox('Multiple Bar Plots', value=True, key="multiple_bar_plots")
        if st.session_state.multiple_bar_plots:
            chosen_options.append("Multiple Bar Plots")
        st.checkbox(t("text_answer"), value=True, key="text_answer")
        if st.session_state.text_answer:
            chosen_options.append("Text Antwort")
    if n_answers == 3:
        st.checkbox("3D Plot", value=True, key="3d_plot")
        if st.session_state["3d_plot"]:
            chosen_options.append("3D Plot")
        st.checkbox(t("multiple_bar_plots"), value=True, key="multiple_bar_plots")
        if st.session_state.multiple_bar_plots:
            chosen_options.append("Multiple Bar Plots")
        st.checkbox(t("text_answer"), value=True, key="text_answer")
        if st.session_state.text_answer:
            chosen_options.append("Text Antwort")
    if n_answers > 3:
        st.checkbox(t("multiple_bar_plots"), value=True, key="multiple_bar_plots")
        if st.session_state.multiple_bar_plots:
            chosen_options.append("Multiple Bar Plots")
        st.checkbox(t("text_answer"), value=True, key="text_answer")
        if st.session_state.text_answer:
            chosen_options.append("Text Antwort")
    if "selected_figs" not in st.session_state:
        st.session_state.selected_figs = None

    if st.button(t("show_result"), key="show_result_button"):
        st.session_state.selected_figs = chosen_options

    return st.session_state.selected_figs
        # Collect chosen options

# input_visualisation()

def input_part():

    st.text_input(t("enter_question"), key="question", #value = "",
            disabled=st.session_state.confirmed)

    question = st.session_state.question

    answers = input_answers()
    if answers is None:
        return None

    n_answers = len(answers)

    min_max = input_min_max(n_answers)
    if min_max is None:
        return None

    mini, maxi = min_max

    st.checkbox(t("anonym"), key="anonym", value=False)

    if n_answers == 2:
        df = input_vote_2(answers, question, mini, maxi)
    else:
        df = input_vote_many(answers, question, mini, maxi)

    if not st.session_state.get("finished", False):
        return None
    figs = input_visualisation(n_answers)

    return df, figs, n_answers, answers, question, mini, maxi

def plot_bar(df, question, answers):
    names = df['Name'].tolist()
    values = df['Answer'].to_numpy()

    colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, len(values))
    )

    fig, ax = plt.subplots(figsize=(9.2, 1))
    ax.invert_yaxis()

    negative_sum = np.sum(values[values < 0])
    positive_sum = np.sum(values[values > 0])
    abs_max = np.max((negative_sum*-1, positive_sum))
    total = negative_sum + positive_sum

    ax.set_xlim(-abs_max, abs_max)
    ax.set_xticks(range(-abs_max, abs_max + 1))
    ax.set_yticks([])
    ax.set_title(question, fontsize=14, fontweight='bold', pad=15, loc='left')
    # Remove Box from plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)

    ax.text(0, -0.5, answers[0], transform=ax.transAxes, ha='left', va='center', fontsize=12)
    ax.text(1, -0.5, answers[1], transform=ax.transAxes, ha='right', va='center', fontsize=12)

    pos_cum = 0
    neg_cum = negative_sum

    for name, value, color in zip(names, values, colors):

        if value > 0:
            start = pos_cum
            pos_cum += value
        elif value < 0:
            start = neg_cum - value
            neg_cum -= value
        else:
            start = 0

        rects = ax.barh(" ", value, left=start, height=0.5, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'

        if not st.session_state.anonym:
            ax.bar_label(rects, labels=[name], label_type='center', color=text_color)
    # ax.bar_label(rects, labels=[name], label_type='center', color=text_color)
    ax.vlines(0, -0.5, 0.5, color='black', linewidth=0.8)
    ax.vlines(total, -0.5, 0.5, color='Red', linewidth=2)
    ax.text(total, -0.8, t("public_opinion"), transform=ax.transData, ha='center', va='top', fontsize=10, color='Red')
    st.pyplot(fig)
    # plt.show()
    
def plot_coord(df, question, answers, maxi):
    # make a 3d coordinate system with points for the position of each person and a mean point
    # Add the Durchschnitt row
    df_avg = pd.DataFrame({'Name': t("public_opinion"), 
                        **{df.columns[1:][i]: df[df.columns[1:][i]].mean() 
                            for i in range(len(df.columns[1:]))}}, index=[0])
    df_fin = pd.concat([df, df_avg], ignore_index=True)

    if not st.session_state.anonym:
        # Format the names with rounded values
        for i in range(len(df_fin['Name'])):
            df_fin.loc[i, 'Name'] = f"{df_fin.loc[i, 'Name']} ({round(df_fin.iloc[i,1],2)}|{round(df_fin.iloc[i,2],2)}|{round(df_fin.iloc[i,3],2)})"
    else:
        # If anonym, replace names with "Participant 1", "Participant 2", etc.
        for i in range(len(df_fin['Name'])-1):  # exclude the last row (average)
            df_fin.loc[i, 'Name'] = f"{t('participants')} {i+1}"
    # Convert Names to categorical codes
    names = df_fin['Name'].astype('category')
    codes = names.cat.codes
    unique_names = names.cat.categories

    # Create color map
    cmap = plt.get_cmap('tab10')  # use tab10 or tab20 for more participants
    n_colors = len(unique_names)
    colors = cmap(codes / (n_colors - 1 if n_colors > 1 else 1))  # normalize to [0,1]

    # Data
    xs = pd.to_numeric(df_fin[answers[0]], errors='coerce').to_numpy()
    ys = pd.to_numeric(df_fin[answers[1]], errors='coerce').to_numpy()
    zs = pd.to_numeric(df_fin[answers[2]], errors='coerce').to_numpy()

    # Wider figure with GridSpec
    fig = plt.figure(figsize=(14,8))  # wider figure
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 0.3], figure=fig)
    ax = fig.add_subplot(gs[0], projection='3d')

    # Scatter plot
    scatter = ax.scatter(xs, ys, zs, c=colors, s=60, depthshade=False)
    min_val = 0
    max_val = maxi

    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    ax.set_zlim(min_val, max_val)
    ax.set_box_aspect([1,1,1])  # maintain cube aspect ratio

    # Create legend handles
    handles = [mlines.Line2D([0], [0], marker='o', color='w',
                            markerfacecolor=cmap(i / (n_colors - 1 if n_colors > 1 else 1)),
                            markersize=8)
            for i in range(n_colors)]

    # Place legend outside the axes
    ax.legend(handles, unique_names, title=t("participants"), loc='center left',
            bbox_to_anchor=(1.05, 0.8), fontsize=10)
    
    
    st.checkbox(t("show_guide_lines"), value=False, key="guide_lines")
    
    if st.session_state.guide_lines:
        
        # Projection lines for all points except the average
        for i in range(len(xs)-1):  # exclude the last point (average)
            ax.plot([xs[i], xs[i]], [ys[i], 0], [zs[i], 0], color="#767676", linestyle='-.', alpha=0.4)
            ax.plot([xs[i], 5], [ys[i], ys[i]], [zs[i], 0], color='#767676', linestyle='-.', alpha=0.4)
            ax.plot([xs[i], 5], [ys[i], 5], [zs[i], zs[i]], color='#767676', linestyle='-.', alpha=0.4)

    # Average point coordinates
    avg_x, avg_y, avg_z = xs[-1], ys[-1], zs[-1]

    st.checkbox(t("show_guide_lines_average_point"), value=True, key="guide_lines_avg")
    
    if st.session_state.guide_lines_avg:
        # Projection lines for average point
        ax.plot([avg_x, avg_x], [avg_y, 0], [avg_z, 0], color='gray', linestyle='--', alpha=0.7)
        ax.plot([avg_x, 5], [avg_y, avg_y], [avg_z, 0], color='gray', linestyle='--', alpha=0.7)
        ax.plot([avg_x, 5], [avg_y, 5], [avg_z, avg_z], color='gray', linestyle='--', alpha=0.7)

        # Highlight the max axis with red line
        if avg_x >= avg_y and avg_x >= avg_z:
            ax.plot([avg_x, avg_x], [avg_y, 0], [avg_z, 0], color='red', linestyle='--', alpha=0.7)
        if avg_y >= avg_x and avg_y >= avg_z:
            ax.plot([avg_x, 5], [avg_y, avg_y], [avg_z, 0], color='red', linestyle='--', alpha=0.7)
        if avg_z >= avg_x and avg_z >= avg_y:
            ax.plot([avg_x, 5], [avg_y, 5], [avg_z, avg_z], color='red', linestyle='--', alpha=0.7)

    # Highlight average point
    ax.scatter(avg_x, avg_y, avg_z, color='red', s=110)

    # Axis ticks
    ax.set_xticks(range(min_val, max_val + 1))
    ax.set_yticks(range(min_val, max_val + 1))
    ax.set_zticks(range(min_val, max_val + 1))

    # Labels
    ax.set_title(question, fontsize=14, fontweight='bold', pad=15, loc='left')
    ax.set_xlabel(answers[0])
    ax.set_ylabel(answers[1])
    ax.set_zlabel(answers[2])
    ax.zaxis.label.set_rotation(90)
    st.pyplot(fig)
    # plt.show()


def plot_waage(df, question, answers):
    # Separate negatives and positives
    df_neg = df[df['Answer'] < 0].copy()
    df_neg = df_neg.sort_values('Answer')  # sort negatives by value
    df_pos = df[df['Answer'] > 0].copy()
    df_pos = df_pos.sort_values('Answer', ascending=False)  # sort positives by value
    
    # Total weights
    left_weight = df_neg['Answer'].abs().sum()
    right_weight = df_pos['Answer'].abs().sum()
    
    # Beam settings
    width = 4
    height = 1.15
    max_tilt = np.pi / 8  # max ~22.5 degrees
    total = left_weight + right_weight
    # Invert tilt so heavier side goes down
    angle = max_tilt * (left_weight - right_weight)/total if total != 0 else 0
    
    # Beam endpoints
    x0, y0 = -width/2, height
    x1, y1 = width/2, height
    cx, cy = 0, height
    
    # Rotate function
    def rotate(x, y):
        xr = cx + (x-cx)*np.cos(angle) - (y-cy)*np.sin(angle)
        yr = cy + (x-cx)*np.sin(angle) + (y-cy)*np.cos(angle)
        return xr, yr
    
    x0r, y0r = rotate(x0, y0)
    x1r, y1r = rotate(x1, y1)
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    # Draw beam
    ax.plot([x0r, x1r], [y0r, y1r], color='saddlebrown', lw=6, zorder=2)
    # Support
    ax.plot([0,0], [0,height], color='black', lw=5, zorder=1)
    # Make a proper stand which looks like wide at the bottom and narrow at the top
    ax.add_patch(patches.Polygon([(-0.5,0), (0.5,0), (0.2,0.5), (-0.2,0.5)], color='black', zorder=1))
    ax.add_patch(patches.Circle((0,height), 0.06, color='black', zorder=3))
    
    # Draw pans
    pan_size = 0.5
    ax.add_patch(patches.Rectangle((x0r-pan_size, y0r), 2*pan_size, 0.1*pan_size, color='black', zorder=3))
    ax.add_patch(patches.Rectangle((x1r-pan_size, y1r), 2*pan_size, 0.1*pan_size, color='black', zorder=3))
    ax.add_patch(patches.Wedge((x0r, y0r), 0.2*pan_size, 180,0, color='black', zorder=2))
    ax.add_patch(patches.Wedge((x1r, y1r), 0.2*pan_size, 180,0, color='black', zorder=2))
    
    ax.text(x0r, 0.1, answers[0], ha='center', va='top', fontsize=16)
    ax.text(x1r, 0.1, answers[1], ha='center', va='top', fontsize=16)
    # Colors for each participant
    names = df['Name'].tolist()
    cmap = plt.get_cmap('tab10')
    colors = {name:cmap(i/len(names)) for i,name in enumerate(names)}
    
    max_abs = df['Answer'].abs().max()
    
    # Function to plot a square above a pan, rotated with the beam
    def plot_square(x_beam, y_beam, value, name, idx):
        # offset vertically above pan
        offset = 0.15 + idx*0.2
        x0s, y0s = rotate(x_beam, y_beam + offset)
        x0s = x_beam
        size = 1000 * abs(value) / max_abs
        ax.scatter(x0s, y0s, s=size, color=colors[name], marker='s', zorder=3)
        if not st.session_state.anonym:
            ax.text(x0s, y0s, name, ha='center', va='bottom', fontsize=10, rotation=0, zorder=4)
    # Plot negative squares on left
    for i, row in enumerate(df_neg.itertuples()):
        plot_square(x0, y0, row.Answer, row.Name, i)
    
    # Plot positive squares on right
    for i, row in enumerate(df_pos.itertuples()):
        plot_square(x1, y1, row.Answer, row.Name, i)
    
    # Legend
    handles = [mlines.Line2D([0],[0], marker='s', color='w', markerfacecolor=color, markersize=10) 
               for color in colors.values()]
    # ax.legend(handles, names, title='Teilnehmer', bbox_to_anchor=(1.05,0.5), loc='center left')
    
    # Axis
    ax.set_xlim(-width/2-0.5, width/2+0.5)
    ax.set_ylim(0, height+1.2)
    ax.axis('off')
    ax.set_title(question, fontsize=14, fontweight='bold', pad=15, loc='left')
    st.pyplot(fig)
    # plt.show()

def plot_many_bars(df, question, answers):
    participants = df.Name.tolist()
    if len(answers) == 2:
        df[answers[0]] = df['Answer'].where(df['Answer'] > 0, 0)
        df[answers[1]] = df['Answer'].where(df['Answer'] < 0, 0).abs()
        df = df.drop(columns=['Answer'])
    results = {}
    for i in range(df.shape[1]-1):
        results[df.columns[i+1]] = df.iloc[:, i+1].to_list()
    
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)

    category_colors = plt.colormaps['tab10'](np.linspace(0.15, 0.85, data.shape[1]))
    
    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    ax.set_title(question, fontsize=14, fontweight='bold', pad=15, loc='left')
    # Remove Box from plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    

    for i, (partic, color) in enumerate(zip(participants, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=partic, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        # print(partic, len(rects))
        labels_for_rects = [
            partic if w != 0 else ""
            for w in widths
        ]
        if not st.session_state.anonym:
            ax.bar_label(rects, labels=labels_for_rects, label_type='center', color=text_color)

    # # Calculate total for each category
    # totals = df.iloc[:, 1:df.shape[1]].sum(axis=0)
    # # totals
    # winner = totals.idxmax()
    # winner_idx_num = df.columns.get_loc(winner) - 1  # adjust for Name column

    # ax.text(totals[winner]/2, winner_idx_num-0.4, "Option " + winner + 'winner_option_2', va='center', ha='left', fontsize=12, color='Red')
    # # Draw a red box around the winner
    # ax.add_patch(patches.Rectangle((0, winner_idx_num-0.3), totals[winner], 0.6, fill=False, edgecolor='red', linewidth=2))
    st.pyplot(fig)
    # plt.show()

def opinion_text_n2(df):
    strongest_answer = max(df['Answer'])
    weakest_answer = min(df['Answer'])
    strongest_opinion = df[df['Answer'] == strongest_answer]['Name'].tolist()
    weakest_opinion = df[df['Answer'] == weakest_answer]['Name'].tolist()

    if len(strongest_opinion) == 1:
        st.write(t("strong_opinion_1", name=strongest_opinion[0]))
    elif len(strongest_opinion) == 2:
        st.write(t("strong_opinion_2", name1=strongest_opinion[0], name2=strongest_opinion[1]))
    else:
        st.write(t("strong_opinion_more", names=", ".join(strongest_opinion[:-1]) + " " + t("and") + " " + strongest_opinion[-1]))
    
    if len(weakest_opinion) == 1:
        st.write(t("weak_opinion_1", name=weakest_opinion[0]))
    elif len(weakest_opinion) == 2:
        st.write(t("weak_opinion_2", name1=weakest_opinion[0], name2=weakest_opinion[1]))
    else:
        st.write(t("weak_opinion_more", names=", ".join(weakest_opinion[:-1]) + " " + t("and") + " " + weakest_opinion[-1]))

def opinion_text_more(df, mini, maxi):
    meani =(maxi - mini)/2 + mini
    values = df.iloc[:, 1:].astype(float)

    df["magnitude"] = (values - meani).abs().sum(axis=1)
    strongest_answer = max(df['magnitude'])
    weakest_answer = min(df['magnitude'])
    strongest_opinion = df[df['magnitude'] == strongest_answer]['Name'].tolist()
    weakest_opinion = df[df['magnitude'] == weakest_answer]['Name'].tolist()

    if len(strongest_opinion) == 1:
        st.write(t("strong_opinion_1", name=strongest_opinion[0]))
    elif len(strongest_opinion) == 2:
        st.write(t("strong_opinion_2", name1=strongest_opinion[0], name2=strongest_opinion[1]))
    else:
        st.write(t("strong_opinion_more", names=", ".join(strongest_opinion[:-1]) + " " + t("and") + " " + strongest_opinion[-1]))
    
    if len(weakest_opinion) == 1:
        st.write(t("weak_opinion_1", name=weakest_opinion[0]))
    elif len(weakest_opinion) == 2:
        st.write(t("weak_opinion_2", name1=weakest_opinion[0], name2=weakest_opinion[1]))
    else:
        st.write(t("weak_opinion_more", names=", ".join(weakest_opinion[:-1]) + " " + t("and") + " " + weakest_opinion[-1]))

def repeat_vote():
    st.write(t("repeat_vote"))
    col1, col2 = st.columns(2)

    with col1:
        st.button(t("yes_with_same"), key="repeat_same_settings", on_click=lambda: st.session_state.update(finished=False, votes=[], selected_figs=[]))

    with col2:
        st.button(t("yes_with_new"), key="repeat_new_settings", on_click=lambda: st.session_state.update(finished=False, votes=[], confirmed=False, confirmed_min_max=False, answers=["", ""], selected_figs=[]))
        
def repeat_vote_fin():
    st.write(t("repeat_vote"))
    col1, col2, col3 = st.columns(3)

    with col1:
        st.button(t("yes_with_same"), key="repeat_same_settings_fin", on_click=lambda: st.session_state.update(finished=False, votes=[], selected_figs=None))

    with col2:
        st.button(t("yes_with_new"), key="repeat_new_settings_fin", on_click=lambda: st.session_state.update(finished=False, votes=[], confirmed=False, confirmed_min_max=False, answers=["", ""], selected_figs=None))
    with col3:
        st.button(
            t("no"),
            key="repeat_no_fin",
            on_click=lambda: st.session_state.update(app_state="finished")
        )

def text_answer(df, n_answers, answers, mini, maxi):
    if n_answers == 2:
        result = df.iloc[:,1:].sum(axis=0).values[0]
        
        if result < 0:
            st.write(t('winner_option', winner=answers[0]))
            if not st.session_state.anonym:
                opinion_text_n2(df)
            
        elif result == 0:
            st.write(t('draw'))
            repeat_vote()

        else:
            st.write(t('winner_option', winner=answers[1]))
            if not st.session_state.anonym:
                opinion_text_n2(df)
    else:
        totals = df.iloc[:, 1:df.shape[1]].sum(axis=0)
        winners = totals[totals == totals.max()].index.tolist()
        if len(winners) == 1:
            st.write(t('winner_option', winner=winners[0]))
            if not st.session_state.anonym:
                opinion_text_more(df, mini, maxi)
        elif len(winners) == 2:
            st.write(t('draw_2', winner1=winners[0], winner2=winners[1]))
            repeat_vote()
        else:
            st.write(t('draw_more', winners=", ".join(winners[:-1]) + " " + t("and") + " " + winners[-1]))
            repeat_vote()

def reset_vote_state():
    keys_to_keep = ["lang"]  # keep language
    
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]

def praeferenz():
    if st.session_state.app_state == "finished":
        st.write(t("vote_finished"))
        st.button(
            t("back_to_start"),
            on_click=reset_vote_state
        )
        # if st.button(t("back_to_start")):
        #     st.session_state.clear()
        #     st.rerun()
        return
    if st.session_state.app_state == "voting":
        result = input_part()
        if result is None:
            return

        df, figs, n_answers, answers, question, mini, maxi = result
        if figs is None:
            return

        if "Bar Plot" in figs:
            plot_bar(df, question, answers)
        if "Waage" in figs:
            plot_waage(df, question, answers)
        if "3D Plot" in figs:
            plot_coord(df, question, answers, maxi)
        if "Multiple Bar Plots" in figs:
            plot_many_bars(df, question, answers)
        if "Text Antwort" in figs:
            text_answer(df, n_answers, answers, mini, maxi)
        if st.session_state.selected_figs:
            # st.write(t("vote_finished"))
            # st.button(t("back_to_start"), on_click=lambda: st.session_state.update(answer="", confirmed=False, app_state="finished"))
            st.button(
                t("finish"),
                on_click= lambda: st.session_state.update(app_state="finished"))#reset_vote_state
            # )
            # repeat_vote_fin()
praeferenz()