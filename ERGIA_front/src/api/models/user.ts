export interface User {
  email: string;
  first_name: string;
  last_name: string;
  id_user: string;
  password?: string; 
}


export interface UpdateUserDTO {
  firstname?: string;
  lastname?: string;
  email?: string;
  password?: string;
}
