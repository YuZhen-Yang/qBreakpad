#include <QCoreApplication>
#include <QBreakpadHandler.h>
#include <cstdio>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    printf("qBreakpad version: %s\n", qPrintable(QBreakpadHandler::version()));
    return 0;
}
