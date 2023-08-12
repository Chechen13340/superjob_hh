from superjob_hh.src.functions import del_info, display_top_vacncies

if __name__ == "__main__":
    choice_platform = input('Выберите платформу для получения данных (HH/SJ): ')
    get_data = del_info(choice_platform)
    display_top = display_top_vacncies(choice_platform)
