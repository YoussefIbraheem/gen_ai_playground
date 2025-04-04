import streamlit as st
from database import create_task, get_tasks, update_task, delete_task , get_session , Task


def main():
    st.title("Task Manager")
    
    session = get_session()
    
    menu_items = ["View", "Create", "Update", "Delete"]
    choice = st.sidebar.selectbox("Select an option", menu_items)
    
    if choice:
        st.subheader(f"{choice} Task")
        match choice:
            case "Create":
                title = st.text_input("Task Title")
                description = st.text_area("Task Description")
                
                if st.button("Create Task"):
                   create_task(title, description)
            case "View":
                tasks = get_tasks()
                for task in tasks:
                    st.title(task.title)
                    st.text(task.description)
                    st.html("<hr>")
            case "Update":
                selected_task_id = st.number_input("Task Number",min_value=1,step=1)
                task = session.query(Task).filter_by(id=selected_task_id).first()
                if task:
                    new_title = st.text_input("New Title",value=task.title)
                    new_description = st.text_input("New Description",value=task.description)
                    confirm_update = st.button("update",key=task.id)
                    if confirm_update:
                        update_task(task.id,new_title,new_description)
                        st.success("Updated Successfully!")
                else:
                    st.warning("We couldn't find the task please try again :(")
            case "Delete":
                  selected_task_id = st.number_input("Task Number",min_value=1,step=1)
                  task = session.query(Task).filter_by(id=selected_task_id).first()
                  if task:
                    st.title(task.title)
                    st.text(task.description)
                    confirm_delete = st.button("Delete")
                  else:
                      st.warning("We couldn't find the task please try again :(")  
                  if confirm_delete:
                        delete_task(task.id)
                        st.success("Deleted Successfully!")
                        
                        
        
main()                    
    