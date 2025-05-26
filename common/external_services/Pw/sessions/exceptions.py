# common/sessions/exceptions.py
import functools
import logging
import aiohttp
import asyncio

class HttpRequestException(Exception):
    """Eccezione generica per errori HTTP"""
    pass

class NetworkException(HttpRequestException):
    """Errore di rete (es. DNS, connessione)"""
    pass

class TimeoutException(HttpRequestException):
    """Errore di timeout"""
    pass

class CancelledRequest(HttpRequestException):
    """Interruzione manuale (Ctrl+C)"""
    pass

def exception_handler(log_errors=False):
    """Decoratore per gestire errori asincroni e fare log"""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)

            except asyncio.TimeoutError:
                if log_errors:
                    logging.error("Timeout durante la richiesta")
                raise TimeoutException("Timeout nella richiesta")

            except aiohttp.ClientConnectionError as e:
                if log_errors:
                    logging.error(f"Errore di rete: {e}")
                raise NetworkException("Errore di rete")

            except aiohttp.ClientError as e:
                if log_errors:
                    logging.error(f"Errore HTTP generico: {e}")
                raise HttpRequestException(f"Errore HTTP: {str(e)}")

            except KeyboardInterrupt:
                if log_errors:
                    logging.warning("Richiesta interrotta manualmente")
                raise CancelledRequest("Operazione annullata")

            except Exception as e:
                if log_errors:
                    logging.exception("Errore sconosciuto")
                raise HttpRequestException(f"Errore sconosciuto: {str(e)}")

        return wrapper
    return decorator
