export const getCookie = (name: string) => {
    const cookies = document.cookie.split(";");

    for (const cookie of cookies) {
        const [cname, value] = cookie.split("=");
        if (cname.trim() === name) {
            return value;
        }
    }

    return "";
};

export const getCsrfToken = () => getCookie("csrftoken");
