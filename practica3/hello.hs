main = do
    putStrLn "Hello, everybody"
    putStrLn ("Please look at my favorite odd numbers: " ++ show (filter odd [10..20]))
    putStrLn ("Como se usa haskell")
    putStrLn ("Primero descargue haskell")
    putStrLn ("en los links dados por el profesor")
    putStrLn ("despues pase a otros videos")
    putStrLn ("para ver sus funciones y comandos")

    putStrLn("Y agregue una entrada de usuario")
    putStrLn "Escribe tu nombre:"
    nombre <- getLine
    putStrLn ("Mucho gusto, " ++ nombre)


