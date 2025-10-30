"""
Práctica 4: Sistema musculoesqueletico

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Ana Kamila Valle Z. Flores
Número de control: 22211769
Correo institucional: l22211769@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,6,3
n = round((tend - t0)/dt) + 1
t = np.linspace(t0,tend,n)
u = np.zeros(n); u[round(1/dt):round(2/dt)] = 1

# Componentes del circuito RLC y función de transferencia
R,Cs,Cp,a =100, 10E-6, 100E-6, 0.25
numControl = [R * Cs, 1-a]
denControl = [R * (Cp + Cs), 1]
sysControl = ctrl.tf(numControl, denControl)
print(f"Función de transferencia del sistema: {sysControl}")

R = 10E3
numCaso = [R * Cs, 1-a]
denCaso = [R * (Cp + Cs), 1]
sysCaso = ctrl.tf(numCaso, denCaso)
print(f"Función de transferencia del sistema: {sysCaso}")

Cr = 1E-6
Re = 1/(28350.2753909505*Cr)
Rr = 0.0320097289384142*Re
numPI = [Rr*Cr,1]
denPI = [Re*Cr,0]
PI = ctrl.tf(numPI,denPI)
print(f"Función de transferencia del controlador: {PI}")

X = ctrl.series(PI, sysCaso)
sysPI = ctrl.feedback(X, 1, sign = -1)
print(f"Función de transeferencia del sistema de control de lazo cerrado {sysPI}")
sysTratamiento = ctrl.series(sysControl, sysPI)




# Respuesta del sistema en lazo abierto y en lazo cerrado
clr1 = np.array([85,107,47])/255
clr2 = np.array([154,63,63])/255
clr3 = np.array([27,60,83])/255
clr4 = np.array([152,161,188])/255
clr5 = np.array([51,56,160])/255


_,Fs1 =ctrl.forced_response(sysControl,t,u,x0)
_,Fs2 =ctrl.forced_response(sysCaso,t,u,x0)

fg1 = plt.figure()
plt.plot(t,u,'-',linewidth=1,color=clr1,label='F(t):Señal')
plt.plot(t,Fs1,'-',linewidth=1,color=clr2,label='Fs1(t):Control')
plt.plot(t,Fs2,'-',linewidth=1,color=clr3,label='Fs2(t):Caso')
plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.2,1.2); plt.yticks(np.arange(-0.2,1.3,0.2))
plt.xlabel('F(t) [V]')
plt.ylabel('t [s]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('sistema musculoesqueletico python.png',dpi=600,bbox_inches='tight')
fg1.savefig('sistema musculoesqueletico python.pdf')

_,Fs3 =ctrl.forced_response(sysTratamiento,t,u,x0)

fg2 = plt.figure()
plt.plot(t,u,'-',linewidth=1,color=clr1,label='F(t):Señal')
plt.plot(t,Fs1,'-',linewidth=1,color=clr2,label='Fs1(t):Contro')
plt.plot(t,Fs2,'-',linewidth=1,color=clr4,label='Fs2(t):Caso')
plt.plot(t,Fs3,'--',linewidth=1,color=clr4,label='Fs3(t):Tratamiento')
plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.2,1.2); plt.yticks(np.arange(-0.2,1.3,0.2))
plt.xlabel('F(t) [V]')
plt.ylabel('t [s]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg2.set_size_inches(w,h)
fg2.tight_layout()
fg2.savefig('sistema musculoesqueletico python PI.png',dpi=600,bbox_inches='tight')
fg2.savefig('sistema musculoesqueletico python PI.pdf')
    