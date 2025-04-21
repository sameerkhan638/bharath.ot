def optimize_timetable():
    # Entities
    courses = ["Math", "Physics", "Chemistry", "English", "Biology"]
    teachers = ["T1", "T2", "T3"]
    rooms = ["R1", "R2", "R3"]
    timeslots = [
        "D1_T1", "D1_T2", "D1_T3", "D1_T4", "D1_T5",
        "D2_T1", "D2_T2", "D2_T3", "D2_T4", "D2_T5"
    ]

    # Create binary variables: 1 if course c is scheduled in slot s with teacher t and room r
    x = LpVariable.dicts("Schedule", (courses, teachers, rooms, timeslots), cat=LpBinary)

    # Create model
    model = LpProblem("Timetable_Optimization", LpMinimize)

    # Objective function: Minimize total assignments (just a placeholder objective)
    model += lpSum(x[c][t][r][s] for c in courses for t in teachers for r in rooms for s in timeslots)

    # Constraint 1: Each course must be scheduled exactly once
    for c in courses:
        model += lpSum(x[c][t][r][s] for t in teachers for r in rooms for s in timeslots) == 1

    # Constraint 2: A teacher can’t be in two places at the same time
    for t in teachers:
        for s in timeslots:
            model += lpSum(x[c][t][r][s] for c in courses for r in rooms) <= 1

    # Constraint 3: A room can’t be used by more than one course at a time
    for r in rooms:
        for s in timeslots:
            model += lpSum(x[c][t][r][s] for c in courses for t in teachers) <= 1

    # Constraint 4: Teacher T3 not available on D1_T1 and D2_T5
    for s in ["D1_T1", "D2_T5"]:
        for c in courses:
            for r in rooms:
                model += x[c]["T3"][r][s] == 0

    # Solve the problem
    model.solve()

    # Extract results
    schedule = []
    for c in courses:
        for t in teachers:
            for r in rooms:
                for s in timeslots:
                    if x[c][t][r][s].varValue == 1:
                        schedule.append([c, t, r, s])

    # Create DataFrame
    df_schedule = pd.DataFrame(schedule, columns=["Course", "Teacher", "Room", "Timeslot"])
    return df_schedule

# Streamlit UI
def main():
    st.title("📘 School Timetable Optimization")

    st.write("""
    This app optimizes a school timetable using linear programming (PuLP).
    Click the button below to generate the timetable.
    """)

    if st.button("Optimize Timetable"):
        with st.spinner("Optimizing..."):
            df_schedule = optimize_timetable()
            st.success("Timetable generated successfully!")
            st.dataframe(df_schedule)

            # Optional: Download link
            csv = df_schedule.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Timetable as CSV", csv, "timetable_output.csv", "text/csv")

if __name__ == "__main__":
    main()
