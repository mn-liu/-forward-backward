import numpy as np

#前向算法计算
def forword(A, B, pi, o, status, N):
    # 计算初值
    # alpha(1)(i) = pi_i*b_i(o_1)
    #status为状态个数，N为初始状态盒子的个数
    alpha = np.zeros((status, N))
    for i in range(N):
        x = o[0]#o为状态序列，o[0]代表了初始的状态，0为红色球，1为白色球
        alpha[0][i] = pi[i] * B[i][x]
    #递推计算
    for T in range(status-1):
        z = o[T+1]
        for i in range(N):
            a = 0
            for j in range(N):
                a += (alpha[T][j] * A[j][i])
            alpha[T+1][i] = a * B[i][z]
    #终止
    P = 0  #概率初始化为0
    for i in range(N):
        P += alpha[status-1][i]
    return P, alpha

def backword(A, B, pi, o, status, N):
    #设置初值，beta_t(i)=1
    beta = np.ones((status, N))
    #递推
    for t in range(status-1):
        h = o[status - t - 1]
        for i in range(N):
            beta[t][i] = 0
            for j in range(N):
                beta[t][i] += A[i][j] * B[j][h] * beta[t+1][j]
    #终止
    P = 0
    for i in range(N):
        z = o[0]
        P += pi[i] * B[i][z] * beta[0][i]
    return P, beta

if __name__ == "__main__":
    A = [[0.5, 0.1, 0.4], [0.3, 0.5, 0.2], [0.2, 0.2, 0.6]]
    B = [[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]]
    pi = [0.2, 0.3, 0.5]
    O = ['红', '白', '红', '红', '白', '红', '白', '白']
    status = 8
    N = 3
    o = np.zeros(status, np.int)
    for i in range(status):
        if O[i] == '红':
            o[i] = 0
        else:
            o[i] = 1
    P_forword, alpha = forword(A, B, pi, o, status, N)
    P_backword, beta = backword(A, B, pi, o, status, N)
    print("前向概率:", P_forword)
    print("后向概率:", P_backword)
    #P(i4=q3|O,lameda) = alpah_4(3)* beta_4(3)
    P = alpha[3][2] * beta[3][2]
    print("前向后向概率计算可得 P(i4=q3|O,lambda)=", P / P_forword)
