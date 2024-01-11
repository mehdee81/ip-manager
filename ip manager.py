import subprocess as sp

class NetworkConfig:
    def __init__(self, connection_name="not set"):
        self.connection_name = connection_name

        
    def set_dns(self, preferred_dns, alternate_dns):
        try:
            prog = sp.Popen(["netsh" ,"interface" ,"ipv4" ,"add" ,"dnsserver" ,f'{self.connection_name}',f"address={preferred_dns}","index=1"],stdin=sp.PIPE)
            prog.communicate()
            
            if alternate_dns.lower() != "none":
                prog = sp.Popen(["netsh" ,"interface" ,"ipv4" ,"add" ,"dnsserver" ,f'{self.connection_name}',f"address={alternate_dns}","index=2"],stdin=sp.PIPE)
                prog.communicate()
            
            print("DNS servers set successfully.")
        except sp.CalledProcessError as e:
            print(f"Error setting DNS servers: {e}")

    def set_ip(self, input):
        try:
            if len(input.split(" "))== 1:
                prog = sp.Popen(["netsh" ,"interface" ,"ipv4" ,"set" ,"address" ,f'{self.connection_name}',"static",f"{input}"],stdin=sp.PIPE)
                prog.communicate()

            elif len(input.split(" "))== 2:
                prog = sp.Popen(["netsh" ,"interface" ,"ipv4" ,"set" ,"address" ,f'{self.connection_name}',"static",f"{input.split(' ')[0]}" , "255.255.255.0" ,f"{input.split(' ')[1]}"],stdin=sp.PIPE)
                prog.communicate()
                
            print("ip address set successfully.")
        except sp.CalledProcessError as e:
            print(f"Error setting DNS servers: {e}")
    def start(self):
        print(f"""
            
                    This program is created by mahdi momeni.
                    Select one of commands.
                    
                    [1] Set Shecan dns.
                    [2] Set other dns.
                    [3] Set ip address.
                    [4] Flush DNS (Clear dns).
                    [5] Clear ip address.
                    [6] Change Connection Name.
                    [7] Exit program.
            
                    connection name: can be Wi-Fi or Ethernet.       
            """)


config = NetworkConfig("not set")
config.start()
while (True):

    if config.connection_name == "not set":
        print("a: Wi-Fi | b: Ethernet")
        conn = input("Select connection name: ")
        if conn == 'a':
            config = NetworkConfig("Wi-Fi")
        elif conn == 'b':
            config = NetworkConfig("Ethernet")
        else:
            print("write a or b.")
    else:
        command = input("command: ")

        if command == '1':

            preferred_dns_server = "178.22.122.100"  
            alternate_dns_server = "185.51.200.2"
            config.set_dns(preferred_dns_server, alternate_dns_server)

        elif command == '2':
        
            preferred_dns_server = input("Preferred Dns Server: ")
            alternate_dns_server = input("Alternate Dns Server (this can be None | write None): ")
            if preferred_dns_server != alternate_dns_server: 
                config.set_dns(preferred_dns_server, alternate_dns_server)
            else:
                print("Preferred and Alternate dns server have not be equal.")    
        
        elif command == '3':
            print("write Ip Address then Gateway (Gateway can be empty)")
            print("sample : 192.168.1.100 192.168.1.1")
            ip_g = input("ip and gateway: ")
            config.set_ip(ip_g)
        elif command == '4':
            prog = sp.Popen(["netsh" ,"interface" ,"ip" ,"set" ,"dns" ,f'{config.connection_name}',"dhcp"],stdin=sp.PIPE)
            prog.communicate()
            print("dns server has been removed")
        elif command == '5':
            prog = sp.Popen(["netsh" ,"interface" ,"ip" ,"set" ,"address" ,f'{config.connection_name}',"dhcp"],stdin=sp.PIPE)
            prog.communicate()
            print("ip address has been removed")
        elif command == '6':
            config.connection_name = "not set"
        elif command == '7':
            exit()
        else:
            print("This is not a correct command.")