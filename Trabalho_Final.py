import tkinter
import socket
import threading
import tkinter.messagebox

class Tela(tkinter.Tk):
    def IniciarTela(self):
        self.title("Zap Zap Chat")
        self.geometry("800x800")
        self.resizable(False, False)
        
        self.CentralizarAplicacao()
        self.CriarComponentes()
        self.IniciarVariaveis()
        self.mainloop()
    
    def IniciarVariaveis(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def CentralizarAplicacao(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def CriarComponentes(self):
        self.ConfigurarDadosConexao()
        self.ConfigurarChat()
        
    def ConfigurarDadosConexao(self):   
        self.labelframe_conexao = tkinter.LabelFrame(self, text="Dados de Conexão ", font=("Arial", 18))
        self.labelframe_conexao.place(x=10, y=10, width=780, height=150)

        # Dados do Servidor
        self.label_destino_ip = tkinter.Label(self.labelframe_conexao, text="Destino IP:", font=("Arial", 12, "bold"))
        self.label_destino_ip.place(x=2, y=2, width=100, height=30)
        self.entry_destino_ip = tkinter.Entry(self.labelframe_conexao, justify="center", font=("Arial", 12))
        self.entry_destino_ip.place(x=100, y=2, width=200, height=30)  

        self.label_destino_porta = tkinter.Label(self.labelframe_conexao, text="Porta:", font=("Arial", 12, "bold"))
        self.label_destino_porta.place(x=310, y=2, width=100, height=30)
        self.entry_destino_porta = tkinter.Entry(self.labelframe_conexao, justify="center", font=("Arial", 12))
        self.entry_destino_porta.place(x=410, y=2, width=100, height=30)
        
        # # Dados da Máquina Local
        self.label_local_ip = tkinter.Label(self.labelframe_conexao, text="Local IP:", font=("Arial", 12, "bold"))
        self.label_local_ip.place(x=2, y=40, width=100, height=30)
        self.entry_local_ip = tkinter.Entry(self.labelframe_conexao, justify="center", font=("Arial", 12))
        self.entry_local_ip.place(x=100, y=40, width=200, height=30)

        self.label_local_porta = tkinter.Label(self.labelframe_conexao, text="Porta:", font=("Arial", 12, "bold"))
        self.label_local_porta.place(x=310, y=40, width=100, height=30)
        self.entry_local_porta = tkinter.Entry(self.labelframe_conexao, justify="center", font=("Arial", 12))
        self.entry_local_porta.place(x=410, y=40, width=100, height=30)

        # self.var_servidor = tkinter.BooleanVar()
        # self.check_servidor = tkinter.Checkbutton(self.labelframe_conexao, text="Ser Servidor", font=("Arial", 12), variable=self.var_servidor)
        # self.check_servidor.place(x=10, y=75)

        self.ConfigurarDadosConexaoBotoes()

    def ConfigurarDadosConexaoBotoes(self):
        self.button_conectar = tkinter.Button(self.labelframe_conexao, text="Conectar", font=("Arial", 12, "bold"), fg="green")
        self.button_conectar.place(x=670, y=75, width=100, height=30)
        self.button_conectar["command"] = self.Conectar 
    
        self.button_desconectar = tkinter.Button(self.labelframe_conexao, text="Desconectar", font=("Arial", 12, "bold"), fg="red")
        self.button_desconectar.place(x=555, y=75, width=110, height=30)
        self.button_desconectar["command"] = self.Desconectar   

        self.button_limpar = tkinter.Button(self.labelframe_conexao, text="Limpar", font=("Arial", 12, "bold"))
        self.button_limpar.place(x=200, y=75, width=100, height=30)
        self.button_limpar["command"] = self.Limpar

    def ConfigurarChat(self):
        self.labelframe_chat = tkinter.LabelFrame(self, text="Chat ", font=("Arial", 18))
        self.labelframe_chat.place(x=10, y=170, width=780, height=350)

        self.text_chat = tkinter.Text(self.labelframe_chat, font=("Arial", 18), height=10, width=50)
        self.text_chat.place(x=10, y=10, width=760, height=300)

        self.label_mensagem = tkinter.Label(self, text="Mensagem:", font=("Arial", 18))
        self.label_mensagem.place(x=10, y=530)
        
        self.entry_mensagem = tkinter.Entry(self, font=("Arial", 16))
        self.entry_mensagem.place(x=10, y=560, width=780, height=30)

        self.button_enviar = tkinter.Button(self, text="Enviar", font=("Arial", 16, "bold"))
        self.button_enviar.place(x=690, y=600, width=100, height=30)
        self.button_enviar["command"] = self.EnviarMensagem

    def EnviarMensagem(self):
        mensagem = self.entry_mensagem.get()

        # if self.var_servidor.get():
        #     self.cliente.send(mensagem.encode('utf-8'))
        # else:
        self.cliente_socket.send(mensagem.encode('utf-8'))    
        self.text_chat.insert(tkinter.END, f"Você: {mensagem}\n")
        self.entry_mensagem.delete(0, tkinter.END)

    def Conectar(self):
        destino_ip = self.entry_destino_ip.get()
        destino_porta = int(self.entry_destino_porta.get())

        local_ip = self.entry_local_ip.get()
        local_porta = int(self.entry_local_porta.get())

        resposta = tkinter.messagebox.askquestion("Conexão", "Confirme os dados de conexão, estão corretos?" + 
                        f"\nServidor: {destino_ip}:{destino_porta}" +
                        f"\nLocal: {local_ip}:{local_porta}", icon="question")
        
        if resposta == 'no':
            return
        

        self.server_socket.bind((local_ip, local_porta))
        server_thread = threading.Thread(target=self.Server)
        server_thread.start()

        conectou = False
        while not conectou:
            try:
                self.cliente_socket.connect((destino_ip, destino_porta))
                conectou = True
            except:
                pass
        # self.cliente_socket.connect((local_ip, local_porta))
        local_thread = threading.Thread(target=self.Cliente)
        local_thread.start()

    def Desconectar(self): 
        self.finalizar_server = True
        self.finalizar_cliente = True
        self.text_chat.insert(tkinter.END, "Desconectado...\n")

    def Limpar(self):   
        self.entry_servidor_ip.delete(0, tkinter.END)
        self.entry_local_ip.delete(0, tkinter.END)
        self.entry_servidor_ip.focus()

    def Server(self):
        print('Ligando o servidor...')
        self.server_socket.listen()
        self.cliente, self.endereco = self.server_socket.accept()

        self.finalizar_server = False
        self.text_chat.insert(tkinter.END, f"Conectado com {self.endereco}\n")

        while not self.finalizar_server:
            mensagem = self.cliente.recv(1024).decode('utf-8')
            
            if mensagem.strip() == '':
                continue
            
            self.text_chat.insert(tkinter.END, f"Cliente: {mensagem}\n")
            
        self.cliente.close()
        self.server_socket.close()

    def Cliente(self):
        self.finalizar_cliente = False

        while not self.finalizar_cliente:
            True
            # mensagem = self.cliente_socket.recv(1024).decode('utf-8')
            # self.text_chat.insert(tkinter.END, f"Servidor: {mensagem}\n")
        
        self.cliente_socket.close()



Applicacao = Tela()
Applicacao.IniciarTela()