import { createTheme } from "@mui/material";

export const theme = createTheme(
    {
        palette: {
            primary: {
              main: "#2a9461"
            },
            secondary: {
              main: "#494c7d"
            },
            primaryLight: {
              main: "#dbece2",
              contrastText: "#616161"
            }
          },
        typography: {
          body1: {
            fontFamily: 'Roboto',
          },
          fontFamily: 'Bangers',
          caption: {
            fontFamily: 'Do Hyeon',
          },
          overline: {
            fontFamily: 'Do Hyeon',
          },
          body2: {
            fontFamily: 'Roboto',
          },
        },
        components: {
            MuiSelect: {
                styleOverrides: {  
                    select: {
                      fontSize: "1.2rem",
                        backgroundColor: "#dbece2",
                       
                    },

                },
            },
            MuiFormControl: {
                styleOverrides: {
                    root: { 
                        backgroundColor: "#dbece2aa", 
                        
                    }
                }
            },
            MuiMenuItem:{
                styleOverrides: {  
                    root: {
                      fontSize: "1.2rem",
                      ":hover":{
                          backgroundColor: "#dbece280",
                      },
                      "&.Mui-selected": {

                          backgroundColor: "#dbece2ff",
                      }
                    }
                }
            },
            MuiInputBase: {
                styleOverrides: {
                    root: {
                        height: "36.5px"
                    }
                }

            }

        }
      } 
);